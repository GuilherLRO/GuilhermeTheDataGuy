import json
import requests
import os
import csv

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"
INPUT_CSV = "input_items.csv"  # Ensure this file exists with headers: Merchant, Item, Brand, Categories
OUTPUT_CSV = "classified_items.csv"
NUM_TRIALS = 20  # Number of times to run the prompt for each item
TEMPERATURE = 0.8 # Increase temperature to see variation (0 is deterministic)

PROMPT_TEMPLATE = """
Classify this item as Apparel, Footwear, or None.

Merchant: {merchant}
Item: {item}
Brand: {brand}
Categories: {categories}

Rules (Examples are not exhaustive):
- Apparel: Clothing (shirts, pants, dresses, jackets, bras, underwear,etc.). Exclude socks, swimwear, sleepwear.
- Footwear: Shoes, boots, sandals, cleats, etc. Exclude socks.
- None: Accessories, equipment, out-of-scope items.

Answer: <Apparel|Footwear|None>
Reasoning: <brief>
"""

def classify_item(merchant, item, brand, categories):
    prompt = PROMPT_TEMPLATE.format(
        merchant=merchant,
        item=item,
        brand=brand,
        categories=categories
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
        print(f"Error classifying item {item}: {e}")
        return f"Error: {e}"

def main():
    if not os.path.exists(INPUT_CSV):
        # Create a sample input file if it doesn't exist to demonstrate
        print(f"File {INPUT_CSV} not found. Creating a sample one...")
        with open(INPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Merchant", "Item", "Brand", "Categories"])
            writer.writeheader()
            writer.writerow({
                "Merchant": "nike",
                "Item": "air jordan 12 retro \"white & game royal\" men's shoes",
                "Brand": "Nike",
                "Categories": "men > footwear > lifestyle"
            })
            writer.writerow({
                "Merchant": "nike",
                "Item": "nike sportswear club fleece hoodie",
                "Brand": "Nike",
                "Categories": "men > clothing > hoodies"
            })

    all_results = []
    
    with open(INPUT_CSV, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f_out:
        
        reader = csv.DictReader(f_in)
        # Add new columns for the trial number and the raw output
        fieldnames = reader.fieldnames + ["Trial", "Ollama_Output"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            for trial in range(1, NUM_TRIALS + 1):
                print(f"Processing: {row['Item']} (Trial {trial}/{NUM_TRIALS})...")
                result = classify_item(
                    row.get("Merchant", ""),
                    row.get("Item", ""),
                    row.get("Brand", ""),
                    row.get("Categories", "")
                )
                
                output_row = row.copy()
                output_row["Trial"] = trial
                output_row["Ollama_Output"] = result
                writer.writerow(output_row)
                
                # Store for summary
                all_results.append({
                    "item": row.get("Item", ""),
                    "trial": trial,
                    "summary": result[:30].replace("\n", " ")
                })
                print(f"Result (Trial {trial}): {result[:50]}...")

    print(f"\nFinished! Results saved to {OUTPUT_CSV}")
    
    # Print the "nice" summary at the end
    print("\n" + "="*80)
    print(f"{'ITEM (truncated)':<35} | {'TRIAL':<5} | {'FIRST 20 CHARS'}")
    print("-" * 80)
    for res in all_results:
        print(f"{res['item'][:33]:<35} | {res['trial']:<5} | {res['summary']}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
