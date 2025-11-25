from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_LOGIC"))


def analyze_file_logic(filename: str, patch: str) -> list:
    """
    Analyze logical correctness of a single file's code changes.
    
    Args:
        filename: Name of the file being reviewed
        patch: The diff patch content
    
    Returns:
        List of logic issues in JSON format
    """
    prompt = f"""You are a Logic Review Agent for GitHub Pull Requests.

Your task:
Analyze only the LOGICAL correctness of the code changes in the patch below.
Focus strictly on logic bugs, incorrect conditions, wrong return values, code that may break, or potential unintended behavior.

Input:
- File: {filename}
- Code Patch:
{patch}

Rules:
1. Consider ONLY the changed lines shown in the patch.
2. Ignore style, formatting, readability, and security issues.
3. Identify real logic problems that could cause incorrect program behavior.
4. Reference the exact line numbers from the patch when possible.
5. If no logic issues exist, return an empty list [].

Output Format:
Return ONLY valid JSON in this exact format:

[
  {{
    "line": <line_number or null>,
    "issue": "<short logic issue>",
    "suggestion": "<how to fix it>"
  }}
]

Important:
- NO explanations outside JSON.
- NO markdown.
- Keep comments short and actionable."""
    
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    return response.text



