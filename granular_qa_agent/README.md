# LLM-Based Data Validation

A tool for validating product classification data using OpenAI's LLMs. It validates L1-L3 hierarchy, Gender, and FoP (Field of Play) classifications against defined documentation.

## Setup

```bash
cd granular_qa_agent

# Install dependencies
uv sync

# Set your OpenAI API key in parent directory
echo "OPENAI_API_KEY=sk-your-key-here" > ../.env
```

## Usage Examples

### Basic Examples

```bash
# Test with 5 rows (sequential)
python run_validation.py --limit 5

# Test with 10 rows using faster/cheaper model
python run_validation.py --model gpt-4o-mini --limit 10

# Output as CSV instead of JSON
python run_validation.py --limit 10 --format csv --output results.csv
```

### Parallel Processing (Faster)

```bash
# 20 rows with 4 parallel workers (~4x faster)
python run_validation.py -m gpt-4o-mini -l 20 -p 4

# 50 rows with 5 workers, CSV output
python run_validation.py -m gpt-4o-mini -l 50 -p 5 -f csv -o results.csv

# Process all rows with 5 workers
python run_validation.py -m gpt-4o-mini -p 5 -f csv -o results.csv
```

### Resume / Skip Existing

```bash
# Resume interrupted run (automatically skips already processed items)
python run_validation.py -m gpt-4o-mini -p 4 -f csv -o results.csv

# Force reprocess everything (ignore existing output)
python run_validation.py -m gpt-4o-mini -p 4 --no-skip -f csv -o results.csv
```

### Quick Start Recommendation

```bash
python run_validation.py -m gpt-4o-mini -l 10 -p 3 -f csv -o results.csv
```

## Command Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--input` | `-i` | `data_sample.csv` | Input CSV file path |
| `--output` | `-o` | `validation_results.json` | Output file path |
| `--format` | `-f` | `json` | Output format: `json` or `csv` |
| `--model` | `-m` | `gpt-4o` | OpenAI model to use |
| `--limit` | `-l` | None | Limit number of rows to process |
| `--parallel` | `-p` | `1` | Number of parallel workers |
| `--no-skip` | - | False | Reprocess all items, ignore existing |

## Model Recommendations

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| `gpt-4o-mini` | ⚡ Fast | $ | Good | Daily validation, testing |
| `gpt-4o` | ⚡ Fast | $$ | Excellent | Production, high accuracy |
| `gpt-4-turbo` | Medium | $$$ | Excellent | Complex cases |

## Parallel Workers Recommendation

| Workers | Use Case |
|---------|----------|
| 1 | Debugging, see each row in order |
| 3-5 | Normal usage, good balance |
| 10 | Maximum speed (may hit rate limits) |

⚠️ **Note:** OpenAI has rate limits. If you see rate limit errors, reduce the number of workers.

## Output Format

Each validated row contains:

```json
{
  "item_key": "nike_mens_running_shorts",
  "merchant": "nike",
  "web_categories": "men > apparel > running",
  "l1": "Apparel",
  "l2": "Bottoms",
  "l3": "null",
  "gender": "Men's",
  "primary_fop": "null",
  "sub_sport": "null",
  "l1_validated": "Apparel",
  "l2_validated": "Bottoms",
  "l3_validated": "Shorts",
  "gender_validated": "Men's",
  "primary_fop_validated": "running",
  "sub_sport_validated": null,
  "corrected_columns": ["l3", "primary_fop"],
  "reasoning": "L3 should be Shorts. FoP is running based on web category."
}
```

### Output Fields

| Field | Description |
|-------|-------------|
| `*_validated` | LLM's validated classification |
| `corrected_columns` | List of original column names that were corrected |
| `reasoning` | Explanation of corrections made |

## Programmatic Usage

```python
from validator import validate_rows, validate_csv

# Validate a single row
row = {
    "item_key": "nike_mens_running_shorts",
    "merchant": "nike",
    "web_categories": "men > apparel > running",
    "l1": "Apparel",
    "l2": "Bottoms",
    "l3": "null",
    "gender": "Men's",
    "primary_fop": "null",
    "sub_sport": "null"
}
results = validate_rows([row], model="gpt-4o-mini")
print(results)

# Validate CSV file
results = validate_csv(
    input_path="data_sample.csv",
    output_path="results.json",
    model="gpt-4o-mini",
    limit=10,
    parallel=3
)
```

## Classification Documentation

The validator uses these documentation files:

- `L1-L3 Hierarchy Definitions.md` - Product type hierarchy
- `Gender Classification Definitions.md` - Gender classification rules
- `FoP Definitions.md` - Field of Play (sport/activity) definitions
- `Values Reference Tables.md` - Valid values for all fields

## Files

| File | Description |
|------|-------------|
| `validator.py` | Main validation module |
| `run_validation.py` | CLI runner script |
| `data_sample.csv` | Sample input data |
| `results.csv` / `*.json` | Validation output |






