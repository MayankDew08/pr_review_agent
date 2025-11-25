from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_PERFORMANCE"))


def analyze_file_performance(filename: str, patch: str) -> list:
    """
    Analyze performance aspects of a single file's code changes.
    
    Args:
        filename: Name of the file being reviewed
        patch: The diff patch content
        
    
    Returns:
        List of performance issues in JSON format
    """
    prompt = f"""You are a Performance Review Agent for GitHub Pull Requests.

Your job is to analyze ONLY the PERFORMANCE aspects of the code changes in the PATCH below.

Detect performance bottlenecks such as:
- unnecessary loops
- repeated database queries inside loops
- expensive operations inside hot paths
- redundant computations
- inefficient data structures
- non-optimal API calls
- blocking operations
- synchronous I/O where async is better
- excessive object creation
- unbounded recursion
- high complexity (O(n²), O(n³)) where avoidable
- large in-memory operations
- redundant string concatenation in loops
- non-memoized expensive function calls

Input:
File: {filename}

Patch:
{patch}

Rules:
1. Consider ONLY the modified lines in the patch.
2. Ignore logic, security, and readability issues.
3. Identify ONLY genuine performance inefficiencies.
4. Reference exact line numbers when possible.
5. If no performance issues exist, return [].

Return STRICT JSON ONLY in this format:

[
  {{
    "line": <line number or null>,
    "severity": "<low|medium|high>",
    "issue": "<performance bottleneck>",
    "suggestion": "<performance improvement>",
    "fixed_code": "<optimized code snippet or null>"
  }}
]

Important:
- No markdown.
- No extra explanations.
- Keep suggestions short and actionable."""
    
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    return response.text



