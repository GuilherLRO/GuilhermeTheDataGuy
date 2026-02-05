import json
import requests
import os
import csv
import random
from collections import Counter
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"
INPUT_CSV = "items_sport_validation_1.csv"
OUTPUT_CSV = "sport_validation_results.csv"
SUMMARY_CSV = "sport_validation_summary.csv"  # Most common answer per item
NUM_TRIALS = 3  # Number of times to run the prompt for each item
TEMPERATURE = 0.7  # Temperature for variation (0.0 = most consistent/deterministic)
MAX_ITEMS = 10  # Maximum number of items to process (None = all items)
RANDOMIZE_ORDER = True  # Randomize the order of items

# Default possible categories if not provided in CSV
DEFAULT_CATEGORIES = ["sportswear", "running", "basketball", "training", "soccer", "hiking", "golf", "tennis"]

VALIDATION_PROMPT_TEMPLATE = """You are a validator for item-to-sport classification.

Your task: Determine if this item belongs to ONE category from the candidate list.

Candidates: {possible_categories}

DECISION RULES - Follow in order:

1. Choose the MOST SPECIFIC category you can confidently identify:
   - If there is explicit, unmistakable sport-specific terminology → choose that specific sport
   - If there is evidence for a category but not enough for a specific sport → choose the less specific but appropriate category (e.g., "sportswear", "training" if those are in the list)
   - If the evidence is too vague or ambiguous → return "None"

2. When uncertain between multiple specific options, choose the one most securely indicated by the evidence.

3. If you can identify a broader category (like "sportswear" or "training") but not a specific sport, that is acceptable and preferred over "None" when there is reasonable evidence.

Item to validate:
- Merchant: {merchant}
- Website categories: {website_categories}
- Item description: {item_description}

REMEMBER: You can choose less specific categories when appropriate. Only return "None" if there is truly insufficient evidence for any category.

Output format (use exactly this):
Answer: None
Reasoning: Brief explanation
Confidence: Low | Medium

OR if you can identify a category:

Answer: [one category from list]
Reasoning: Specific evidence
Confidence: High | Medium
"""

def validate_sport(merchant, web_categories, item_description, possible_categories):
    prompt = VALIDATION_PROMPT_TEMPLATE.format(
        merchant=merchant,
        website_categories=web_categories if web_categories else "Not provided",
        item_description=item_description,
        possible_categories=possible_categories
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        console.print(f"[bold red]✗ Error validating item:[/bold red] {e}")
        return f"Error: {e}"

def parse_answer(response_text):
    """Extract the Answer value from the response."""
    for line in response_text.split('\n'):
        if line.strip().lower().startswith("answer:"):
            answer = line.split(":", 1)[1].strip()
            # Remove quotes and angle brackets
            answer = answer.replace('"', '').replace('<', '').replace('>', '')
            return answer
    return "Unknown"

def main():
    if not os.path.exists(INPUT_CSV):
        console.print(f"[bold red]Error: File {INPUT_CSV} not found![/bold red]")
        return
    
    # Display configuration
    console.print(Panel.fit(
        f"[bold cyan]Sport Validation Configuration[/bold cyan]\n\n"
        f"[yellow]Model:[/yellow] {MODEL_NAME}\n"
        f"[yellow]Trials per item:[/yellow] {NUM_TRIALS}\n"
        f"[yellow]Temperature:[/yellow] {TEMPERATURE}\n"
        f"[yellow]Max items:[/yellow] {MAX_ITEMS if MAX_ITEMS else 'All'}\n"
        f"[yellow]Randomize order:[/yellow] {RANDOMIZE_ORDER}",
        title="⚙️  Configuration",
        border_style="cyan"
    ))
    
    all_results = []
    item_analysis = {}  # Track answers per item for analysis
    
    with open(INPUT_CSV, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f_out:
        
        reader = csv.DictReader(f_in)
        
        # Add new columns for the trial number and the raw output
        fieldnames = list(reader.fieldnames) + ["Trial", "Validation_Output", "Parsed_Answer"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        rows = list(reader)
        original_count = len(rows)
        
        # Randomize order if enabled
        if RANDOMIZE_ORDER:
            random.shuffle(rows)
            console.print(f"[green]✓[/green] Randomized item order\n")
        
        # Limit items if MAX_ITEMS is set
        if MAX_ITEMS and MAX_ITEMS < len(rows):
            rows = rows[:MAX_ITEMS]
            console.print(f"[green]✓[/green] Processing {MAX_ITEMS} out of {original_count} items\n")
        
        total_items = len(rows)
        
        for idx, row in enumerate(rows, 1):
            merchant = row.get("merchant", "")
            web_categories = row.get("web_categories", "")
            item_description = row.get("item", "")
            
            # Get possible sports from CSV - support both column names
            possible_sports_raw = row.get("possible_sport", row.get("possible_categories", ""))
            
            if possible_sports_raw:
                try:
                    # Parse JSON array format
                    possible_sports_list = json.loads(possible_sports_raw)
                    possible_categories = ", ".join(possible_sports_list)
                except json.JSONDecodeError:
                    # If not JSON, treat as comma-separated string
                    possible_categories = possible_sports_raw
            else:
                # Fallback to defaults
                possible_categories = ", ".join(DEFAULT_CATEGORIES)
            
            # Initialize item tracking
            item_key = f"{merchant}|{item_description}"
            if item_key not in item_analysis:
                item_analysis[item_key] = {
                    "merchant": merchant,
                    "item": item_description,
                    "web_categories": web_categories,
                    "possible_categories": possible_categories,
                    "answers": []
                }
            
            console.print(f"\n[bold blue]═══ [{idx}/{total_items}] Item Processing ═══[/bold blue]")
            console.print(f"[cyan]Item:[/cyan] {item_description[:60]}")
            console.print(f"[cyan]Merchant:[/cyan] {merchant}")
            console.print(f"[cyan]Categories:[/cyan] {web_categories if web_categories else '[dim]N/A[/dim]'}")
            console.print(f"[yellow]Candidates:[/yellow] {possible_categories}\n")
            
            trial_answers = []
            for trial in range(1, NUM_TRIALS + 1):
                console.print(f"  [dim]Trial {trial}/{NUM_TRIALS}[/dim]", end=" ")
                result = validate_sport(
                    merchant,
                    web_categories,
                    item_description,
                    possible_categories
                )
                
                # Parse the answer
                parsed_answer = parse_answer(result)
                trial_answers.append(parsed_answer)
                
                output_row = row.copy()
                output_row["Trial"] = trial
                output_row["Validation_Output"] = result
                output_row["Parsed_Answer"] = parsed_answer
                writer.writerow(output_row)
                
                # Store for analysis
                item_analysis[item_key]["answers"].append(parsed_answer)
                all_results.append({
                    "item": item_description,
                    "trial": trial,
                    "answer": parsed_answer,
                    "summary": result[:30].replace("\n", " ")
                })
                
                # Color code the answer
                if parsed_answer.lower() == "none":
                    console.print(f"→ [red]{parsed_answer}[/red]")
                elif parsed_answer.lower() == "unknown":
                    console.print(f"→ [magenta]{parsed_answer}[/magenta]")
                else:
                    console.print(f"→ [green]{parsed_answer}[/green]")
            
            # Show quick summary for this item
            answer_counts = Counter(trial_answers)
            most_common = answer_counts.most_common(1)[0]
            consistency = (most_common[1] / NUM_TRIALS) * 100
            
            if consistency == 100:
                console.print(f"[bold green]  ✓ Consistent: {most_common[0]} (100%)[/bold green]")
            elif consistency >= 60:
                console.print(f"[yellow]  ⚠ Majority: {most_common[0]} ({consistency:.0f}%)[/yellow]")
            else:
                console.print(f"[red]  ✗ Inconsistent: Split across {len(answer_counts)} answers[/red]")

    # Write summary CSV with most common answer per item
    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f_summary:
        summary_writer = csv.DictWriter(f_summary, fieldnames=[
            "merchant", "web_categories", "item", "possible_categories",
            "most_common_answer", "frequency", "consistency_pct", "all_answers"
        ])
        summary_writer.writeheader()
        
        for item_key, data in item_analysis.items():
            answer_counts = Counter(data['answers'])
            most_common_answer, most_common_count = answer_counts.most_common(1)[0]
            consistency_pct = (most_common_count / NUM_TRIALS) * 100
            
            # Create a string showing all answers with counts
            all_answers_str = "; ".join([f"{ans}({cnt})" for ans, cnt in answer_counts.most_common()])
            
            summary_writer.writerow({
                "merchant": data['merchant'],
                "web_categories": data['web_categories'],
                "item": data['item'],
                "possible_categories": data['possible_categories'],
                "most_common_answer": most_common_answer,
                "frequency": f"{most_common_count}/{NUM_TRIALS}",
                "consistency_pct": f"{consistency_pct:.1f}%",
                "all_answers": all_answers_str
            })
    
    console.print(Panel.fit(
        f"[bold green]✓ Processing Complete![/bold green]\n\n"
        f"Detailed results: [cyan]{OUTPUT_CSV}[/cyan]\n"
        f"Summary results: [cyan]{SUMMARY_CSV}[/cyan]\n"
        f"Items processed: [yellow]{total_items}[/yellow]\n"
        f"Total API calls: [yellow]{total_items * NUM_TRIALS}[/yellow]",
        title="✅ Success",
        border_style="green"
    ))
    
    # Analysis Section
    console.print("\n[bold magenta]═══════════════════════════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]                    DETAILED ANALYSIS BY ITEM                       [/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════════════════════════[/bold magenta]\n")
    
    for item_key, data in item_analysis.items():
        console.print(f"\n[bold cyan]Item:[/bold cyan] {data['item'][:70]}")
        console.print(f"  [dim]Merchant:[/dim] {data['merchant']}")
        console.print(f"  [dim]Categories:[/dim] {data['web_categories'] if data['web_categories'] else 'N/A'}")
        console.print(f"  [dim]Candidates:[/dim] {data['possible_categories']}")
        
        # Count answer frequency
        answer_counts = Counter(data['answers'])
        total = len(data['answers'])
        
        console.print(f"  [yellow]Answer distribution ({NUM_TRIALS} trials):[/yellow]")
        for answer, count in answer_counts.most_common():
            percentage = (count / total) * 100
            bar_length = int(percentage / 5)
            bar = "█" * bar_length
            
            # Color based on answer type
            if answer.lower() == "none":
                color = "red"
            elif answer.lower() == "unknown":
                color = "magenta"
            else:
                color = "green"
            
            console.print(f"    [{color}]{answer:<20}[/{color}] {count:>2}/{total} ({percentage:>5.1f}%) {bar}")
    
    console.print("\n[bold magenta]═══════════════════════════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]                    FINAL SUMMARY - MOST COMMON ANSWERS            [/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════════════════════════[/bold magenta]\n")
    
    # Create summary table showing most common answer per item
    summary_table = Table(title="Consensus Answer per Item", show_header=True, header_style="bold cyan")
    summary_table.add_column("#", style="dim", width=4)
    summary_table.add_column("Item", style="white", width=45)
    summary_table.add_column("Most Common Answer", style="yellow", width=20)
    summary_table.add_column("Frequency", justify="center", style="cyan", width=12)
    summary_table.add_column("Consistency", justify="center", style="green", width=12)
    
    item_num = 1
    for item_key, data in item_analysis.items():
        answer_counts = Counter(data['answers'])
        most_common_answer, most_common_count = answer_counts.most_common(1)[0]
        consistency_pct = (most_common_count / NUM_TRIALS) * 100
        
        # Truncate item description
        item_display = data['item'][:43] + "..." if len(data['item']) > 43 else data['item']
        
        # Color based on answer type
        if most_common_answer.lower() == "none":
            answer_style = f"[red]{most_common_answer}[/red]"
        elif most_common_answer.lower() == "unknown":
            answer_style = f"[magenta]{most_common_answer}[/magenta]"
        else:
            answer_style = f"[green]{most_common_answer}[/green]"
        
        # Color based on consistency
        if consistency_pct == 100:
            consistency_style = f"[bold green]{consistency_pct:.0f}%[/bold green]"
        elif consistency_pct >= 60:
            consistency_style = f"[yellow]{consistency_pct:.0f}%[/yellow]"
        else:
            consistency_style = f"[red]{consistency_pct:.0f}%[/red]"
        
        summary_table.add_row(
            str(item_num),
            item_display,
            answer_style,
            f"{most_common_count}/{NUM_TRIALS}",
            consistency_style
        )
        item_num += 1
    
    console.print(summary_table)
    
    # Overall statistics
    console.print("\n[bold cyan]Overall Statistics:[/bold cyan]")
    all_consensus_answers = [Counter(data['answers']).most_common(1)[0][0] for data in item_analysis.values()]
    consensus_counts = Counter(all_consensus_answers)
    
    console.print(f"  [yellow]Total items processed:[/yellow] {len(item_analysis)}")
    console.print(f"  [yellow]Total API calls made:[/yellow] {len(all_results)}")
    console.print(f"\n  [cyan]Consensus breakdown:[/cyan]")
    for answer, count in consensus_counts.most_common():
        percentage = (count / len(item_analysis)) * 100
        if answer.lower() == "none":
            console.print(f"    [red]{answer}:[/red] {count} items ({percentage:.1f}%)")
        elif answer.lower() == "unknown":
            console.print(f"    [magenta]{answer}:[/magenta] {count} items ({percentage:.1f}%)")
        else:
            console.print(f"    [green]{answer}:[/green] {count} items ({percentage:.1f}%)")
    
    console.print("\n[bold green]✓ Analysis complete![/bold green]\n")

if __name__ == "__main__":
    main()

