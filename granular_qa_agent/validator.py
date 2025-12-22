"""
LLM-Based Data Validation Program

This module validates product classification data using an LLM to verify
L1-L3 hierarchy, Gender, and FoP (Field of Play) classifications.
"""

import json
import csv
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Classification constants
L1_VALUES = ["Apparel", "Footwear", "None"]
L2_VALUES = {
    "Apparel": ["Bottoms", "Tops", "Jackets & Outerwear", "Bras", "Dresses", "Track Suits", "Underwear", "Other Apparel"],
    "Footwear": [],
    "None": []
}
L3_VALUES = {
    "Bottoms": ["Baselayer Bottoms", "Fleece Bottoms", "Pants", "Shorts", "Skirts", "Tights", "Other Bottoms"],
    "Tops": ["Athletic Shirts & Tees", "Baselayer Tops", "Fleece Tops", "Graphic Tees", "Polos", "Replica Jerseys", "Other Tops"],
    "Jackets & Outerwear": ["Jackets", "Outerwear", "Other Jackets & Outerwear"],
    "Bras": [],
    "Dresses": [],
    "Track Suits": [],
    "Underwear": [],
    "Other Apparel": []
}
GENDER_VALUES = ["Kids", "Men's", "Women's", "Unisex/Undefined"]
FOP_APPAREL_VALUES = [
    "sportswear", "running", "basketball", "training", "soccer", "hiking",
    "ski_snowboard", "golf", "tennis", "american_football", "baseball",
    "softball", "lacrosse", "volleyball", "swimming", "cricket", "pickleball",
    "boxing", "gymnastics", "cheer_dance", "rugby", "wrestling", "field_hockey"
]
FOP_FOOTWEAR_VALUES = [
    "sportswear", "running", "basketball", "training", "soccer", "hiking",
    "walking", "flip_flops", "slides", "outdoor_sandals", "ski_snowboard",
    "golf", "tennis", "american_football", "baseball", "softball", "lacrosse",
    "volleyball", "cricket", "pickleball", "boxing", "cheer_dance", "rugby",
    "wrestling", "field_hockey"
]
SUB_SPORT_VALUES = {
    "sportswear": ["sportswear_running", "sportswear_basketball", "sportswear_tennis", 
                   "sportswear_soccer", "sportswear_skateboarding", "sportswear_outdoor", "sportswear_other"],
    "running": ["trail_running", "road_running", "track_field_running", "running_other"],
    "basketball": ["signature_basketball", "performance_basketball", "basketball_other"],
    "training": ["cross_training", "yoga", "training_other"],
    "soccer": ["outdoor_soccer", "indoor_soccer"]
}


def format_duration(seconds: float) -> str:
    """Format seconds into a human-readable duration string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


@dataclass
class ValidationResult:
    """Represents the validation result for a single row."""
    item_key: str
    merchant: str
    web_categories: str
    # Original values
    l1: Optional[str]
    l2: Optional[str]
    l3: Optional[str]
    gender: Optional[str]
    primary_fop: Optional[str]
    sub_sport: Optional[str]
    # Validated values
    l1_validated: Optional[str]
    l2_validated: Optional[str]
    l3_validated: Optional[str]
    gender_validated: Optional[str]
    primary_fop_validated: Optional[str]
    sub_sport_validated: Optional[str]
    # Correction tracking
    corrected_columns: list
    reasoning: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def load_classification_docs() -> str:
    """Load all classification documentation files."""
    docs_path = Path(__file__).resolve().parent
    
    docs = []
    doc_files = [
        "L1-L3 Hierarchy Definitions.md",
        "Gender Classification Definitions.md",
        "FoP Definitions.md"
    ]
    
    for doc_file in doc_files:
        file_path = docs_path / doc_file
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                docs.append(f"## {doc_file}\n\n{f.read()}")
    
    return "\n\n---\n\n".join(docs)


def build_validation_prompt(row: dict, classification_docs: str) -> str:
    """Build the prompt for LLM validation."""
    
    prompt = f"""You are a product classification expert. Your task is to validate and correct product classifications based on the provided documentation.

## Classification Documentation

{classification_docs}

---

## Product to Validate

**Item Key:** {row.get('item_key', '')}
**Merchant:** {row.get('merchant', '')}
**Web Categories:** {row.get('web_categories', '')}

**Current Classifications:**
- L1: {row.get('l1', 'null')}
- L2: {row.get('l2', 'null')}
- L3: {row.get('l3', 'null')}
- Gender: {row.get('gender', 'null')}
- Primary FoP: {row.get('primary_fop', 'null')}
- Sub-sport: {row.get('sub_sport', 'null')}

---

## Instructions

1. Analyze the item_key, merchant, and web_categories to understand what product this is.
2. Based on the classification documentation, determine the CORRECT values for each classification field.
3. Compare your classifications with the current ones and identify any corrections needed.

## Valid Values Reference

**L1:** Apparel, Footwear, None, null
**L2 (if L1=Apparel):** Bottoms, Tops, Jackets & Outerwear, Bras, Dresses, Track Suits, Underwear, Other Apparel, null
**L2 (if L1=Footwear or None):** null
**L3 (if L2=Bottoms):** Baselayer Bottoms, Fleece Bottoms, Pants, Shorts, Skirts, Tights, Other Bottoms, null
**L3 (if L2=Tops):** Athletic Shirts & Tees, Baselayer Tops, Fleece Tops, Graphic Tees, Polos, Replica Jerseys, Other Tops, null
**L3 (if L2=Jackets & Outerwear):** Jackets, Outerwear, Other Jackets & Outerwear, null
**L3 (other L2 or L1=Footwear/None):** null
**Gender:** Kids, Men's, Women's, Unisex/Undefined, null
**Primary FoP (Apparel):** sportswear, running, basketball, training, soccer, hiking, ski_snowboard, golf, tennis, american_football, baseball, softball, lacrosse, volleyball, swimming, cricket, pickleball, boxing, gymnastics, cheer_dance, rugby, wrestling, field_hockey, null
**Primary FoP (Footwear):** sportswear, running, basketball, training, soccer, hiking, walking, flip_flops, slides, outdoor_sandals, ski_snowboard, golf, tennis, american_football, baseball, softball, lacrosse, volleyball, cricket, pickleball, boxing, cheer_dance, rugby, wrestling, field_hockey, null
**Sub-sport:** Only applicable for certain FoP values (sportswear, running, basketball, training, soccer), otherwise null

---

## Response Format

Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):

{{"l1_validated": "<value or null>", "l2_validated": "<value or null>", "l3_validated": "<value or null>", "gender_validated": "<value or null>", "primary_fop_validated": "<value or null>", "sub_sport_validated": "<value or null>", "corrected_columns": ["<original_column_name>", ...], "reasoning": "<brief explanation of any corrections made>"}}

IMPORTANT:
- Use EXACT values from the valid values lists above
- Use "null" (as a string) for null/missing values
- Only list columns in corrected_columns if you changed their value
- Use ORIGINAL column names in corrected_columns: "l1", "l2", "l3", "gender", "primary_fop", "sub_sport" (NOT the _validated versions)
- If no corrections needed, use an empty list [] for corrected_columns
- Keep reasoning concise but informative
"""
    return prompt


def validate_row(client: OpenAI, row: dict, classification_docs: str, model: str = "gpt-4o") -> ValidationResult:
    """Validate a single row using the LLM."""
    
    prompt = build_validation_prompt(row, classification_docs)
    
    # Build API call parameters
    api_params = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    # Only add temperature for models that support it (GPT-5 models don't)
    if not model.startswith("gpt-5"):
        api_params["temperature"] = 0.0  # Deterministic output
    
    response = client.chat.completions.create(**api_params)
    
    response_text = response.choices[0].message.content.strip()
    
    try:
        llm_result = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {response_text}") from e
    
    # Normalize null values
    def normalize_null(val):
        if val is None or val == "null" or val == "NULL" or val == "":
            return None
        return val
    
    def normalize_original(val):
        if val is None or val == "null" or val == "NULL" or val == "" or val == "None":
            return None
        return val
    
    # Build validation result
    result = ValidationResult(
        item_key=row.get("item_key", ""),
        merchant=row.get("merchant", ""),
        web_categories=row.get("web_categories", ""),
        # Original values
        l1=normalize_original(row.get("l1")),
        l2=normalize_original(row.get("l2")),
        l3=normalize_original(row.get("l3")),
        gender=normalize_original(row.get("gender")),
        primary_fop=normalize_original(row.get("primary_fop")),
        sub_sport=normalize_original(row.get("sub_sport")),
        # Validated values
        l1_validated=normalize_null(llm_result.get("l1_validated")),
        l2_validated=normalize_null(llm_result.get("l2_validated")),
        l3_validated=normalize_null(llm_result.get("l3_validated")),
        gender_validated=normalize_null(llm_result.get("gender_validated")),
        primary_fop_validated=normalize_null(llm_result.get("primary_fop_validated")),
        sub_sport_validated=normalize_null(llm_result.get("sub_sport_validated")),
        # Correction tracking
        corrected_columns=llm_result.get("corrected_columns", []),
        reasoning=llm_result.get("reasoning", "")
    )
    
    return result


def process_single_row(args: tuple) -> ValidationResult:
    """Process a single row - used for parallel execution."""
    client, row, classification_docs, model, index, total = args
    try:
        result = validate_row(client, row, classification_docs, model)
        print(f"  ✓ [{index}/{total}] {row.get('item_key', '')[:40]}...")
        return result
    except Exception as e:
        print(f"  ✗ [{index}/{total}] Error: {e}")
        return ValidationResult(
            item_key=row.get("item_key", ""),
            merchant=row.get("merchant", ""),
            web_categories=row.get("web_categories", ""),
            l1=row.get("l1"),
            l2=row.get("l2"),
            l3=row.get("l3"),
            gender=row.get("gender"),
            primary_fop=row.get("primary_fop"),
            sub_sport=row.get("sub_sport"),
            l1_validated=None,
            l2_validated=None,
            l3_validated=None,
            gender_validated=None,
            primary_fop_validated=None,
            sub_sport_validated=None,
            corrected_columns=["ERROR"],
            reasoning=f"Validation failed: {str(e)}"
        )


def process_rows_parallel(
    client: OpenAI,
    rows: list[dict],
    classification_docs: str,
    model: str,
    max_workers: int
) -> list[ValidationResult]:
    """Process rows in parallel using ThreadPoolExecutor."""
    results = []
    total = len(rows)
    
    # Prepare arguments for each row
    args_list = [
        (client, row, classification_docs, model, i, total)
        for i, row in enumerate(rows, 1)
    ]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {executor.submit(process_single_row, args): args[1] for args in args_list}
        
        # Collect results as they complete
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    return results


def load_existing_results(output_path: str, output_format: str = "json") -> set[str]:
    """
    Load existing item_keys from output file to skip already processed items.
    
    Returns:
        Set of item_keys that have already been processed
    """
    existing_keys = set()
    output_file = Path(output_path)
    
    if not output_file.exists():
        return existing_keys
    
    try:
        if output_format.lower() == "csv":
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("item_key"):
                        existing_keys.add(row["item_key"])
        else:
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if item.get("item_key"):
                        existing_keys.add(item["item_key"])
    except Exception as e:
        print(f"Warning: Could not load existing results from {output_path}: {e}")
    
    return existing_keys


def load_existing_results_data(output_path: str, output_format: str = "json") -> list[dict]:
    """
    Load existing results data from output file.
    
    Returns:
        List of existing result dictionaries
    """
    output_file = Path(output_path)
    
    if not output_file.exists():
        return []
    
    try:
        if output_format.lower() == "csv":
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                results = []
                for row in reader:
                    # Parse corrected_columns back from JSON string
                    if row.get("corrected_columns"):
                        try:
                            row["corrected_columns"] = json.loads(row["corrected_columns"])
                        except json.JSONDecodeError:
                            row["corrected_columns"] = []
                    results.append(row)
                return results
        else:
            with open(output_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load existing results from {output_path}: {e}")
        return []


def validate_csv(
    input_path: str,
    output_path: str,
    model: str = "gpt-4o",
    limit: Optional[int] = None,
    output_format: str = "json",
    skip_existing: bool = True,
    parallel: int = 1
) -> list[ValidationResult]:
    """
    Validate all rows in a CSV file.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output file (JSON or CSV)
        model: OpenAI model to use
        limit: Optional limit on number of rows to process
        output_format: Output format - "json" or "csv"
        skip_existing: If True, skip items already in output file (default: True)
        parallel: Number of parallel workers (1 = sequential, >1 = parallel)
    
    Returns:
        List of ValidationResult objects
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    classification_docs = load_classification_docs()
    
    # Load existing results if skip_existing is enabled
    existing_keys = set()
    existing_results = []
    if skip_existing:
        existing_keys = load_existing_results(output_path, output_format)
        if existing_keys:
            existing_results = load_existing_results_data(output_path, output_format)
            print(f"Found {len(existing_keys)} existing results. Skipping already processed items.")
    
    results = []
    
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if limit:
            rows = rows[:limit]
        
        # Filter out already processed rows
        rows_to_process = [r for r in rows if r.get("item_key") not in existing_keys]
        skipped_count = len(rows) - len(rows_to_process)
        
        if skipped_count > 0:
            print(f"Skipping {skipped_count} already processed items.")
        
        total = len(rows_to_process)
        if total == 0:
            print("All items already processed. Nothing to do.")
            # Return existing results converted to ValidationResult objects
            return [dict_to_validation_result(r) for r in existing_results]
        
        # Timing tracking
        start_time = time.time()
        row_times = []
        
        if parallel > 1:
            # Parallel processing
            print(f"🚀 Running with {parallel} parallel workers...")
            results = process_rows_parallel(
                client, rows_to_process, classification_docs, model, parallel
            )
            row_times = [2.0] * len(results)  # Approximate for parallel
        else:
            # Sequential processing
            for i, row in enumerate(rows_to_process, 1):
                row_start = time.time()
                print(f"Processing row {i}/{total}: {row.get('item_key', '')[:50]}...")
                try:
                    result = validate_row(client, row, classification_docs, model)
                    results.append(result)
                    row_elapsed = time.time() - row_start
                    row_times.append(row_elapsed)
                    
                    # Calculate stats
                    avg_time = sum(row_times) / len(row_times)
                    remaining = total - i
                    eta_seconds = avg_time * remaining
                    eta_formatted = format_duration(eta_seconds)
                    
                    print(f"  ✓ Completed in {row_elapsed:.2f}s | Avg: {avg_time:.2f}s | ETA: {eta_formatted}")
                    
                except Exception as e:
                    row_elapsed = time.time() - row_start
                    row_times.append(row_elapsed)
                    print(f"  ✗ Error in {row_elapsed:.2f}s: {e}")
                    # Create error result
                    error_result = ValidationResult(
                        item_key=row.get("item_key", ""),
                        merchant=row.get("merchant", ""),
                        web_categories=row.get("web_categories", ""),
                        l1=row.get("l1"),
                        l2=row.get("l2"),
                        l3=row.get("l3"),
                        gender=row.get("gender"),
                        primary_fop=row.get("primary_fop"),
                        sub_sport=row.get("sub_sport"),
                        l1_validated=None,
                        l2_validated=None,
                        l3_validated=None,
                        gender_validated=None,
                        primary_fop_validated=None,
                        sub_sport_validated=None,
                        corrected_columns=["ERROR"],
                        reasoning=f"Validation failed: {str(e)}"
                    )
                    results.append(error_result)
        
        # Final timing summary
        total_elapsed = time.time() - start_time
        avg_time = total_elapsed / len(results) if results else 0
        print(f"\n⏱ Timing Summary:")
        print(f"  Total time: {format_duration(total_elapsed)}")
        print(f"  Rows processed: {len(results)}")
        print(f"  Avg time/row: {avg_time:.2f}s")
        if parallel > 1:
            print(f"  Parallel workers: {parallel}")
            print(f"  Effective throughput: {len(results) / total_elapsed:.2f} rows/s" if total_elapsed > 0 else "")
    
    # Combine existing results with new results
    new_results_data = [r.to_dict() for r in results]
    all_results_data = existing_results + new_results_data
    
    # Save all results
    if output_format.lower() == "csv":
        save_results_csv(all_results_data, output_path)
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nValidation complete. Results saved to: {output_path}")
    print(f"  - Existing items: {len(existing_results)}")
    print(f"  - New items processed: {len(results)}")
    print(f"  - Total items: {len(all_results_data)}")
    
    # Return all results as ValidationResult objects
    all_results = [dict_to_validation_result(r) for r in existing_results] + results
    return all_results


def dict_to_validation_result(d: dict) -> ValidationResult:
    """Convert a dictionary back to a ValidationResult object."""
    return ValidationResult(
        item_key=d.get("item_key", ""),
        merchant=d.get("merchant", ""),
        web_categories=d.get("web_categories", ""),
        l1=d.get("l1"),
        l2=d.get("l2"),
        l3=d.get("l3"),
        gender=d.get("gender"),
        primary_fop=d.get("primary_fop"),
        sub_sport=d.get("sub_sport"),
        l1_validated=d.get("l1_validated"),
        l2_validated=d.get("l2_validated"),
        l3_validated=d.get("l3_validated"),
        gender_validated=d.get("gender_validated"),
        primary_fop_validated=d.get("primary_fop_validated"),
        sub_sport_validated=d.get("sub_sport_validated"),
        corrected_columns=d.get("corrected_columns", []),
        reasoning=d.get("reasoning", "")
    )


def save_results_csv(results: list[dict], output_path: str) -> None:
    """Save validation results to CSV format."""
    if not results:
        return
    
    # Prepare data for CSV - convert list to JSON string for corrected_columns
    csv_data = []
    for r in results:
        row = r.copy()
        # Convert corrected_columns list to JSON string for CSV compatibility
        row["corrected_columns"] = json.dumps(row["corrected_columns"])
        csv_data.append(row)
    
    fieldnames = list(csv_data[0].keys())
    
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)


def validate_rows(rows: list[dict], model: str = "gpt-4o") -> list[dict]:
    """
    Validate a list of row dictionaries programmatically.
    
    Args:
        rows: List of dictionaries representing rows to validate
        model: OpenAI model to use
    
    Returns:
        List of validation result dictionaries
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    classification_docs = load_classification_docs()
    
    results = []
    for row in rows:
        try:
            result = validate_row(client, row, classification_docs, model)
            results.append(result.to_dict())
        except Exception as e:
            error_result = {
                "item_key": row.get("item_key", ""),
                "error": str(e)
            }
            results.append(error_result)
    
    return results


def generate_summary_report(results: list[ValidationResult]) -> dict:
    """Generate a summary report of validation results."""
    total = len(results)
    rows_with_corrections = sum(1 for r in results if r.corrected_columns)
    
    # Count corrections by column
    column_corrections = {}
    for r in results:
        for col in r.corrected_columns:
            column_corrections[col] = column_corrections.get(col, 0) + 1
    
    return {
        "total_rows": total,
        "rows_with_corrections": rows_with_corrections,
        "rows_without_corrections": total - rows_with_corrections,
        "correction_rate": f"{(rows_with_corrections / total * 100):.1f}%" if total > 0 else "0%",
        "corrections_by_column": column_corrections
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM-Based Data Validation")
    parser.add_argument("--input", "-i", default="data_sample.csv", help="Input CSV file path")
    parser.add_argument("--output", "-o", default="validation_results.json", help="Output file path")
    parser.add_argument("--format", "-f", default="json", choices=["json", "csv"], help="Output format (json or csv)")
    parser.add_argument("--model", "-m", default="gpt-4o", help="OpenAI model to use")
    parser.add_argument("--limit", "-l", type=int, default=None, help="Limit number of rows to process")
    parser.add_argument("--no-skip", action="store_true", help="Reprocess all items, don't skip existing")
    parser.add_argument("--parallel", "-p", type=int, default=1, help="Number of parallel workers (default: 1 = sequential)")
    
    args = parser.parse_args()
    
    # Resolve paths relative to script directory
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / args.input if not Path(args.input).is_absolute() else Path(args.input)
    output_path = script_dir / args.output if not Path(args.output).is_absolute() else Path(args.output)
    
    results = validate_csv(
        input_path=str(input_path),
        output_path=str(output_path),
        model=args.model,
        limit=args.limit,
        output_format=args.format,
        skip_existing=not args.no_skip,
        parallel=args.parallel
    )
    
    # Print summary
    summary = generate_summary_report(results)
    print("\n=== Validation Summary ===")
    print(f"Total rows processed: {summary['total_rows']}")
    print(f"Rows with corrections: {summary['rows_with_corrections']}")
    print(f"Rows without corrections: {summary['rows_without_corrections']}")
    print(f"Correction rate: {summary['correction_rate']}")
    print("\nCorrections by column:")
    for col, count in sorted(summary['corrections_by_column'].items(), key=lambda x: -x[1]):
        print(f"  {col}: {count}")

