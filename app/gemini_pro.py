import os
import time
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS_TO_TRY = ["gemini-3.5-flash-lite", "gemini-1.5-flash", "gemini-1.5-pro"]

def generate_story(outline: list) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini.

    Args:
        outline (list): A list of strings representing each comic panel's idea.

    Returns:
        str: The generated comic story text or an error message.
    """
    # Format the panel outline as a numbered list for clarity
    formatted_outline = "\n".join([f"{i+1}. {item}" for i, item in enumerate(outline)])

    # Construct the prompt
    prompt = f"""
You're a comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- Include narration and clearly marked character lines.
- Keep each panel self-contained but part of a cohesive story.
"""

    for model_name in MODELS_TO_TRY:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text
            except Exception as e:
                if "503" in str(e) or "404" in str(e):
                    time.sleep(2 * (attempt + 1))
                    continue
                return f"Error generating story: {str(e)}"

    return "Error generating story: Gemini API endpoints are temporarily unavailable."
