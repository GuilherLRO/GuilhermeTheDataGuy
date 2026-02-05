#!/usr/bin/env python3
"""
Run a local Ollama model (llama3.1:8b by default) to classify apparel items by gender.

- Reads a CSV with columns: merchant, web_categories, item
- For each row, runs the LLM N times (default 5)
- Extracts the final label from the model output
- Computes agreement metrics: most_common label count, agreement_rate, all_equal
- Writes a results CSV and prints a summary

Usage:
  python classify_gender_ollama.py --input items.csv --output results.csv
Optional:
  --model llama3.1:8b
  --runs 5
  --temperature 0.7
  --ollama-url http://localhost:11434
"""

import argparse
import csv
import re
import sys
import time
from collections import Counter
from typing import Dict, List, Optional, Tuple

import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

LABELS = ["Womens", "Mens", "Kids", "Unisex", "Undetermined"]
LABEL_SET = {l.lower(): l for l in LABELS}

# Initialize rich console
console = Console()

# Color mapping for labels
LABEL_COLORS = {
    "Womens": "magenta",
    "Mens": "blue",
    "Kids": "yellow",
    "Unisex": "green",
    "Undetermined": "red",
}

PROMPT_TEMPLATE = """You are classifying the TARGET GENDER of a product for apparel analytics.

## Item Information
Item: {item}
Merchant: {merchant}
Web Categories: {web_categories}

## Your task
Decide ONE label:
Womens | Mens | Kids | Unisex | Undetermined

Use ALL available context (item name + web categories + merchant). Do not rely only on keywords.
However, do NOT guess: if the evidence is weak or the item is unclear, choose Undetermined.

## How to reason (use context, not just keywords)
Consider:
- The product type (e.g., jersey, joggers, training pants, life vest, gloves, boots)
- The category path meaning (e.g., "baby & toddler > training pants" strongly implies Kids)
- Common retail conventions (e.g., "juniors" is a women's line)
- Explicit audience phrases ("for men", "for ladies", "youth", "toddlers")
- Whether it is human apparel vs non-human (pet/dog clothing)

## Label definitions
Womens:
- Explicitly women's/ladies OR context strongly indicates women's line (e.g., "juniors" = Womens unless it also clearly says kids/toddler/youth)

Mens:
- Explicitly men's OR context strongly indicates men's line (e.g., "for men", "men's")

Kids:
- Explicitly youth/kids/boys/girls/toddler/baby/infant, OR categories clearly indicate child sizing (e.g., "baby & toddler", "youth baseball pants")

Unisex:
Use Unisex ONLY when you have positive evidence it is not gender-targeted:
- Explicitly says unisex, OR
- Clearly an adult/general item with no gender targeting (including "adult/adults" with no gender marker), OR
- Clearly gender-neutral apparel/accessory (e.g., socks, beanie, cap/hat, gloves, basic tee/hoodie/sweatshirt) with no gender/age targeting

Undetermined:
Use Undetermined when evidence is insufficient or unclear:
- Cryptic item text / SKU-like strings / abbreviations where product type or audience isn't clear
- Items that are commonly gendered but not specified and not clearly gender-neutral (e.g., "jacket", "boots", "joggers" without context)
- Non-human apparel (pet/dog clothing)

## Critical: Unisex vs Undetermined
- Unisex = you have a reason to believe it is intended for all genders (explicit unisex / adult-general / gender-neutral accessory).
- Undetermined = you cannot confidently tell the intended gender from the context.

## Confidence guardrails (avoid hallucination)
- Do NOT infer gender from single letters (e.g., "m", "w") or ambiguous abbreviations.
- If conflicting signals exist, prefer the most specific:
  Kids > Womens/Mens > Unisex.
- If the item is clearly a child product by category or sizing, choose Kids even if the item title is generic.

## Output format (EXACTLY; nothing else)
Classification: <Womens|Mens|Kids|Unisex|Undetermined>
Answer: <Womens|Mens|Kids|Unisex|Undetermined>
Reasoning: <one short sentence referencing the key context used>
"""

# Regex to pull the Answer field robustly
ANSWER_RE = re.compile(r"(?im)^\s*Answer\s*:\s*([A-Za-z]+)\s*$")
CLASS_RE = re.compile(r"(?im)^\s*Classification\s*:\s*([A-Za-z_]+)\s*$")
ANY_LABEL_RE = re.compile(r"(?i)\b(womens|mens|kids|unisex|undetermined)\b")


def canonicalize_label(raw: str) -> Optional[str]:
    if not raw:
        return None
    key = raw.strip().lower()
    return LABEL_SET.get(key)


def extract_label(text: str) -> Optional[str]:
    """
    Prefer `Answer:` line. If absent, try `Classification:`.
    As a last resort, find any label token in the output.
    """
    if not text:
        return None

    m = ANSWER_RE.search(text)
    if m:
        return canonicalize_label(m.group(1))

    m = CLASS_RE.search(text)
    if m:
        # classification might be IN_SCOPE style in other prompts; here we expect our labels
        return canonicalize_label(m.group(1).replace("_", ""))

    m = ANY_LABEL_RE.search(text)
    if m:
        return canonicalize_label(m.group(1))

    return None


def ollama_generate(
    ollama_url: str,
    model: str,
    prompt: str,
    temperature: float,
    seed: Optional[int] = None,
    timeout: int = 120,
    progress_task=None,
) -> str:
    """
    Uses Ollama's /api/generate endpoint.
    """
    url = ollama_url.rstrip("/") + "/api/generate"
    payload: Dict = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if seed is not None:
        payload["options"]["seed"] = seed

    start_time = time.time()
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    elapsed = time.time() - start_time
    
    if progress_task:
        progress, task_id = progress_task
        progress.update(
            task_id,
            description=f"[cyan]LLM call completed ({elapsed:.1f}s)"
        )
    
    return data.get("response", "")


def run_n_times(
    ollama_url: str,
    model: str,
    merchant: str,
    web_categories: str,
    item: str,
    runs: int,
    temperature: float,
    max_parse_retries: int = 2,
    sleep_s: float = 0.0,
    progress=None,
    run_task=None,
) -> Tuple[List[str], List[str]]:
    """
    Returns (labels, raw_outputs)
    labels may include "Undetermined" fallback if parsing fails repeatedly.
    """
    labels: List[str] = []
    outputs: List[str] = []

    base_prompt = PROMPT_TEMPLATE.format(
        item=item or "",
        merchant=merchant or "",
        web_categories=web_categories or "",
    )

    # Truncate item name for display
    item_display = item[:50] + "..." if len(item) > 50 else item

    for i in range(runs):
        if run_task and progress:
            progress.update(
                run_task,
                description=f"[cyan]Run {i+1}/{runs}: {item_display}",
                total=runs,
                completed=i
            )
        
        out = ""
        label = None
        parse_attempts = 0
        for attempt in range(max_parse_retries + 1):
            parse_attempts = attempt + 1
            if run_task and progress:
                progress.update(
                    run_task,
                    description=f"[yellow]Calling LLM (attempt {parse_attempts})..."
                )
            
            out = ollama_generate(
                ollama_url=ollama_url,
                model=model,
                prompt=base_prompt,
                temperature=temperature,
                seed=None,  # leave None to allow natural variation
                progress_task=(progress, run_task) if progress and run_task else None,
            )
            label = extract_label(out)
            if label in LABELS:
                break

        if label not in LABELS:
            label = "Undetermined"
            if run_task and progress:
                progress.update(
                    run_task,
                    description=f"[red]Failed to parse label, using Undetermined"
                )

        labels.append(label)
        outputs.append(out)
        
        # Show label with color
        label_color = LABEL_COLORS.get(label, "white")
        if run_task and progress:
            progress.update(
                run_task,
                description=f"[{label_color}]Run {i+1}/{runs}: {label}",
                advance=1
            )

        if sleep_s > 0:
            time.sleep(sleep_s)

    return labels, outputs


def compute_agreement(labels: List[str]) -> Dict:
    c = Counter(labels)
    most_label, most_count = c.most_common(1)[0]
    all_equal = most_count == len(labels)
    return {
        "labels": labels,
        "most_common_label": most_label,
        "most_common_count": most_count,
        "agreement_rate": most_count / max(1, len(labels)),
        "all_equal": all_equal,
        "label_counts": dict(c),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="items.csv", help="Input CSV path")
    ap.add_argument("--output", default="results.csv", help="Output CSV path (results)")
    ap.add_argument("--model", default="llama3.1:8b", help="Ollama model name")
    ap.add_argument("--runs", type=int, default=5, help="Runs per item")
    ap.add_argument("--temperature", type=float, default=0.7, help="LLM temperature")
    ap.add_argument("--ollama-url", default="http://localhost:11434", help="Ollama base URL")
    ap.add_argument("--sleep", type=float, default=0.0, help="Sleep seconds between runs")
    ap.add_argument("--write-raw", action="store_true", help="Include raw outputs in results (large!)", default=False)
    args = ap.parse_args()

    # Print header
    console.print(Panel.fit(
        "[bold cyan]Gender Classification with Ollama[/bold cyan]",
        border_style="cyan"
    ))
    
    # Display configuration
    config_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    config_table.add_row("[bold]Input CSV:[/bold]", args.input)
    config_table.add_row("[bold]Output CSV:[/bold]", args.output)
    config_table.add_row("[bold]Model:[/bold]", args.model)
    config_table.add_row("[bold]Runs per item:[/bold]", str(args.runs))
    config_table.add_row("[bold]Temperature:[/bold]", str(args.temperature))
    config_table.add_row("[bold]Ollama URL:[/bold]", args.ollama_url)
    console.print(config_table)
    console.print()

    # Basic connectivity check
    console.print("[yellow]Checking Ollama connection...[/yellow]")
    try:
        response = requests.get(args.ollama_url.rstrip("/") + "/api/tags", timeout=10)
        response.raise_for_status()
        console.print("[green]✓[/green] Connected to Ollama successfully")
    except Exception as e:
        console.print(f"[bold red]✗ ERROR:[/bold red] Could not reach Ollama at {args.ollama_url}: {e}")
        sys.exit(1)
    console.print()

    # Load CSV
    console.print(f"[cyan]Loading CSV from {args.input}...[/cyan]")
    rows: List[Dict[str, str]] = []
    try:
        with open(args.input, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            needed = {"merchant", "web_categories", "item"}
            missing = needed - set(reader.fieldnames or [])
            if missing:
                console.print(f"[bold red]✗ ERROR:[/bold red] Missing required columns in CSV: {sorted(missing)}")
                console.print(f"Found columns: {reader.fieldnames}")
                sys.exit(1)
            for r in reader:
                rows.append(r)
        console.print(f"[green]✓[/green] Loaded [bold]{len(rows)}[/bold] items from CSV")
    except FileNotFoundError:
        console.print(f"[bold red]✗ ERROR:[/bold red] File not found: {args.input}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]✗ ERROR:[/bold red] Failed to read CSV: {e}")
        sys.exit(1)
    console.print()

    out_fields = [
        "merchant",
        "web_categories",
        "item",
        "run_labels",
        "most_common_label",
        "most_common_count",
        "agreement_rate",
        "all_equal",
        "counts_womens",
        "counts_mens",
        "counts_kids",
        "counts_unisex",
        "counts_undetermined",
    ]
    if args.write_raw:
        out_fields.append("raw_outputs")

    total = 0
    all_equal_n = 0
    avg_agreement_sum = 0.0
    consensus_counter = Counter()
    start_time = time.time()

    console.print(f"[cyan]Processing [bold]{len(rows)}[/bold] items with [bold]{args.runs}[/bold] runs each...[/cyan]")
    console.print()

    with open(args.output, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=out_fields)
        writer.writeheader()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            # Main progress bar for items
            main_task = progress.add_task(
                "[bold cyan]Processing items...",
                total=len(rows)
            )

            for idx, r in enumerate(rows):
                merchant = (r.get("merchant") or "").strip()
                web_categories = (r.get("web_categories") or "").strip()
                item = (r.get("item") or "").strip()

                # Create a task for runs within this item
                item_display = item[:40] + "..." if len(item) > 40 else item
                run_task = progress.add_task(
                    f"[cyan]Item {idx+1}/{len(rows)}: {item_display}",
                    total=args.runs
                )

                labels, outputs = run_n_times(
                    ollama_url=args.ollama_url,
                    model=args.model,
                    merchant=merchant,
                    web_categories=web_categories,
                    item=item,
                    runs=args.runs,
                    temperature=args.temperature,
                    sleep_s=args.sleep,
                    progress=progress,
                    run_task=run_task,
                )

                # Remove the run task
                progress.remove_task(run_task)

                stats = compute_agreement(labels)
                total += 1
                avg_agreement_sum += stats["agreement_rate"]
                if stats["all_equal"]:
                    all_equal_n += 1
                consensus_counter[stats["most_common_label"]] += 1

                # Show result for this item
                label_color = LABEL_COLORS.get(stats["most_common_label"], "white")
                agreement_emoji = "✓" if stats["all_equal"] else "⚠"
                agreement_color = "green" if stats["all_equal"] else "yellow"
                
                progress.update(
                    main_task,
                    advance=1,
                    description=f"[{agreement_color}]{agreement_emoji} Item {idx+1}/{len(rows)}: [{label_color}]{stats['most_common_label']}[/{label_color}] (agreement: {stats['agreement_rate']:.1%})"
                )

                counts = stats["label_counts"]
                out_row = {
                    "merchant": merchant,
                    "web_categories": web_categories,
                    "item": item,
                    "run_labels": "|".join(labels),
                    "most_common_label": stats["most_common_label"],
                    "most_common_count": stats["most_common_count"],
                    "agreement_rate": f"{stats['agreement_rate']:.3f}",
                    "all_equal": str(stats["all_equal"]),
                    "counts_womens": str(counts.get("Womens", 0)),
                    "counts_mens": str(counts.get("Mens", 0)),
                    "counts_kids": str(counts.get("Kids", 0)),
                    "counts_unisex": str(counts.get("Unisex", 0)),
                    "counts_undetermined": str(counts.get("Undetermined", 0)),
                }
                if args.write_raw:
                    out_row["raw_outputs"] = "\n\n---RUN---\n\n".join(outputs)

                writer.writerow(out_row)

    elapsed_time = time.time() - start_time
    avg_agreement = avg_agreement_sum / max(1, total)

    console.print()
    console.print(Panel.fit(
        "[bold green]Processing Complete![/bold green]",
        border_style="green"
    ))

    # Summary table
    summary_table = Table(title="Summary Statistics", box=box.ROUNDED, show_header=True)
    summary_table.add_column("Metric", style="cyan", no_wrap=True)
    summary_table.add_column("Value", style="bold")

    summary_table.add_row("Items processed", str(total))
    summary_table.add_row("Runs per item", str(args.runs))
    summary_table.add_row("Total LLM calls", str(total * args.runs))
    summary_table.add_row("Time elapsed", f"{elapsed_time:.1f}s")
    summary_table.add_row("Items/sec", f"{total/elapsed_time:.2f}" if elapsed_time > 0 else "N/A")
    summary_table.add_row(
        f"All {args.runs} runs equal",
        f"[green]{all_equal_n}[/green] ([bold]{all_equal_n/max(1,total):.1%}[/bold])"
    )
    summary_table.add_row(
        "Average agreement rate",
        f"[bold]{avg_agreement:.3f}[/bold]"
    )

    console.print(summary_table)
    console.print()

    # Label distribution table
    dist_table = Table(title="Label Distribution", box=box.ROUNDED, show_header=True)
    dist_table.add_column("Label", style="bold")
    dist_table.add_column("Count", justify="right")
    dist_table.add_column("Percentage", justify="right")

    for label in LABELS:
        count = consensus_counter.get(label, 0)
        pct = count / max(1, total)
        label_color = LABEL_COLORS.get(label, "white")
        dist_table.add_row(
            f"[{label_color}]{label}[/{label_color}]",
            str(count),
            f"[bold]{pct:.1%}[/bold]"
        )

    console.print(dist_table)
    console.print()
    console.print(f"[green]✓[/green] Results written to: [bold]{args.output}[/bold]")


if __name__ == "__main__":
    main()