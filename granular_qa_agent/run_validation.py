#!/usr/bin/env python3
"""
Example script to run LLM-based validation on product classification data.

Usage:
    # Validate first 5 rows as a test
    python run_validation.py --limit 5

    # Validate all rows
    python run_validation.py

    # Use a different model
    python run_validation.py --model gpt-4o-mini --limit 10
    
    # Custom input/output paths
    python run_validation.py -i my_data.csv -o my_results.json
    
    # Resume validation (default: skips already processed items)
    python run_validation.py --limit 20  # Will skip items already in output
    
    # Force reprocess all items (ignore existing output)
    python run_validation.py --no-skip
    
    # Run with 4 parallel workers (faster)
    python run_validation.py --parallel 4 --limit 20
    
    # Save progress every 5 rows (batch saving)
    python run_validation.py --batch-size 5 --limit 50
    
    # Combine options
    python run_validation.py -m gpt-4o-mini -p 5 -l 50 -f csv -o results.csv -b 10
"""

from pathlib import Path
from validator import validate_csv, generate_summary_report
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Run LLM-based validation on product classification data"
    )
    parser.add_argument(
        "--input", "-i", 
        default="data_sample.csv", 
        help="Input CSV file path (default: data_sample.csv)"
    )
    parser.add_argument(
        "--output", "-o", 
        default="validation_results.json", 
        help="Output JSON file path (default: validation_results.json)"
    )
    parser.add_argument(
        "--model", "-m", 
        default="gpt-4o", 
        help="OpenAI model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=None, 
        help="Limit number of rows to process (default: all)"
    )
    parser.add_argument(
        "--format", "-f", 
        default="json", 
        choices=["json", "csv"],
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--no-skip", 
        action="store_true",
        help="Reprocess all items, don't skip existing ones in output file"
    )
    parser.add_argument(
        "--parallel", "-p",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1 = sequential)"
    )
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=10,
        help="Save progress every N rows (default: 10, 0 = save only at end)"
    )
    
    args = parser.parse_args()
    
    # Resolve paths relative to script directory
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / args.input if not Path(args.input).is_absolute() else Path(args.input)
    output_path = script_dir / args.output if not Path(args.output).is_absolute() else Path(args.output)
    
    # Run validation (rich logging handles the display)
    results = validate_csv(
        input_path=str(input_path),
        output_path=str(output_path),
        model=args.model,
        limit=args.limit,
        output_format=args.format,
        skip_existing=not args.no_skip,
        parallel=args.parallel,
        batch_size=args.batch_size
    )
    
    # Generate and print detailed correction summary
    summary = generate_summary_report(results)
    
    # Import rich components for final summary
    from rich.console import Console
    from rich.table import Table
    from rich import box
    
    console = Console()
    
    if summary['corrections_by_column']:
        table = Table(
            title="📋 Corrections by Column",
            box=box.ROUNDED,
            border_style="yellow"
        )
        table.add_column("Column", style="cyan", no_wrap=True)
        table.add_column("Count", style="yellow", justify="right")
        table.add_column("Rate", style="dim", justify="right")
        
        for col, count in sorted(summary['corrections_by_column'].items(), key=lambda x: -x[1]):
            pct = (count / summary['total_rows'] * 100) if summary['total_rows'] > 0 else 0
            table.add_row(col, str(count), f"{pct:.1f}%")
        
        console.print()
        console.print(table)
    
    # Final stats
    console.print()
    console.print(f"[dim]Correction rate: [yellow]{summary['correction_rate']}[/] "
                  f"({summary['rows_with_corrections']}/{summary['total_rows']} rows)[/]")


if __name__ == "__main__":
    main()

