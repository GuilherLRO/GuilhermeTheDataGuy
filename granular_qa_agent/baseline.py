from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the parent directory's .env file
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(question, model="gpt-5"
    """
    Sends a message to the OpenAI API and returns the model's answer.

    Args:
        question (str): The question/message to send to the model.
        model (str): The OpenAI model to use (default is gpt-3.5-turbo).

    Returns:
        str: The answer from the model.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
    )

    answer = response.choices[0].message.content.strip()
    return answer

if __name__ == "__main__":
    question = "What is the capital of France?"
    answer = ask_openai(question)
    print(answer)