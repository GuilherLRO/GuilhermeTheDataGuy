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
    
    # Combine options
    python run_validation.py -m gpt-4o-mini -p 5 -l 50 -f csv -o results.csv
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
    
    args = parser.parse_args()
    
    # Resolve paths relative to script directory
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / args.input if not Path(args.input).is_absolute() else Path(args.input)
    output_path = script_dir / args.output if not Path(args.output).is_absolute() else Path(args.output)
    
    print("=" * 60)
    print("LLM-Based Data Validation")
    print("=" * 60)
    print(f"Input file:   {input_path}")
    print(f"Output file:  {output_path}")
    print(f"Model:        {args.model}")
    print(f"Row limit:    {args.limit or 'All rows'}")
    print(f"Format:       {args.format}")
    print(f"Skip existing: {not args.no_skip}")
    print(f"Parallel:      {args.parallel} worker(s)")
    print("=" * 60)
    print()
    
    # Run validation
    results = validate_csv(
        input_path=str(input_path),
        output_path=str(output_path),
        model=args.model,
        limit=args.limit,
        output_format=args.format,
        skip_existing=not args.no_skip,
        parallel=args.parallel
    )
    
    # Generate and print summary
    summary = generate_summary_report(results)
    
    print()
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total rows processed:     {summary['total_rows']}")
    print(f"Rows with corrections:    {summary['rows_with_corrections']}")
    print(f"Rows without corrections: {summary['rows_without_corrections']}")
    print(f"Correction rate:          {summary['correction_rate']}")
    print()
    
    if summary['corrections_by_column']:
        print("Corrections by column:")
        print("-" * 30)
        for col, count in sorted(summary['corrections_by_column'].items(), key=lambda x: -x[1]):
            pct = (count / summary['total_rows'] * 100)
            print(f"  {col:25} {count:5} ({pct:.1f}%)")
    else:
        print("No corrections were made.")
    
    print()
    print("=" * 60)
    print(f"Results saved to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()

