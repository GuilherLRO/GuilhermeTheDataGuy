import sqlite3
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

DB_PATH = "trends.db"
CSV_PATH = "old_and_new_thrends.csv"
REPORT_PATH = "report.md"
IMAGES_DIR = "images"


def init_db():
    """Load CSV into SQLite database if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        print(f"Loading {CSV_PATH} into {DB_PATH}...")
        df = pd.read_csv(CSV_PATH)
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("trends", conn, index=False, if_exists="replace")
        conn.close()
        print("Database initialized.")
    else:
        print("Database already exists.")


def reload_db():
    """Force reload CSV into SQLite database (use when CSV is updated)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing {DB_PATH}.")
    print(f"Loading {CSV_PATH} into {DB_PATH}...")
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("trends", conn, index=False, if_exists="replace")
    conn.close()
    print(f"Database reloaded with {len(df)} rows.")


def query_db(query):
    """Execute a query and return a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


def get_next_question_number():
    """Parse report.md to find the next question number."""
    if not os.path.exists(REPORT_PATH):
        return 1
    
    with open(REPORT_PATH, "r") as f:
        content = f.read()
    
    # Find all question numbers in headers like "## Question 1:" or "## Question 14:"
    matches = re.findall(r"## Question (\d+):", content)
    if not matches:
        return 1
    
    # Return the next number after the highest found
    return max(int(m) for m in matches) + 1


def append_to_report(question, reasoning, sql_query, results_df, raw_question=None, image_path=None, summary=None):
    """
    Append a Q&A entry to the report.md file with auto-numbering and PDF-friendly formatting.
    
    Args:
        question: The optimized question text (goes in header)
        reasoning: Explanation of SQL logic
        sql_query: The SQL query string
        results_df: Pandas DataFrame with query results
        raw_question: The user's original question (optional)
        image_path: Path to visualization image (optional)
        summary: Summary analysis text (optional)
    """
    question_num = get_next_question_number()
    
    with open(REPORT_PATH, "a") as f:
        f.write(f"\n## Question {question_num}: {question}\n")
        if raw_question:
            f.write(f"*Raw question: {raw_question}*\n")
        f.write(f"\n### Reasoning\n{reasoning}\n\n")
        f.write(f"### SQL Query\n```sql\n{sql_query}\n```\n\n")
        
        # Format results as a markdown table
        table = tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False)
        f.write(f"### Results\n\n{table}\n\n")
        
        if image_path:
            # Use relative path for markdown
            rel_image_path = os.path.relpath(image_path, os.path.dirname(REPORT_PATH))
            f.write(f"### Visualization\n![{question}]({rel_image_path})\n\n")

        if summary:
            # PDF-friendly formatting: two blank lines after header, one before separator
            f.write(f"### Summary Analysis\n\n\n{summary}\n\n")
        
        f.write("---\n")
    
    print(f"✓ Added Question {question_num} to report.md")
    return question_num


def generate_chart(df, x, y, title, filename, chart_type="line", hue=None):
    """
    Generate a chart and save it to the images directory.
    
    Args:
        df: Pandas DataFrame with data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        filename: Output filename (saved to images/)
        chart_type: 'line', 'bar', or 'grouped_bar'
        hue: Column for grouping (used with grouped_bar)
    
    Returns:
        Filepath of saved image
    """
    plt.figure(figsize=(10, 6))
    
    if chart_type == "line":
        sns.lineplot(data=df, x=x, y=y, hue=hue)
    elif chart_type == "bar":
        sns.barplot(data=df, x=x, y=y)
    elif chart_type == "grouped_bar":
        # For grouped bar charts comparing old vs new
        sns.barplot(data=df, x=x, y=y, hue=hue)
    
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    
    filepath = os.path.join(IMAGES_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Chart saved to {filepath}")
    return filepath


def clear_images():
    """Remove all images from the images directory."""
    if os.path.exists(IMAGES_DIR):
        for f in os.listdir(IMAGES_DIR):
            if f.endswith('.png'):
                os.remove(os.path.join(IMAGES_DIR, f))
        print("✓ Cleared all images from images/")


if __name__ == "__main__":
    init_db()
