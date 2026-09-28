import os
import json
import time
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS_TO_TRY = ["gemini-3.5-flash-lite", "gemini-1.5-flash", "gemini-1.5-pro"]

def generate_outline(user_prompt: str) -> list:
    """
    Generates a 5-panel comic layout based on the user's story idea using Gemini.

    Args:
        user_prompt (str): The user's comic idea prompt.

    Returns:
        list: A list of dictionaries, one for each panel.
    """
    prompt = f"""
You are a professional AI comic planner.

Your task is to generate a *strictly formatted* JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string)

Respond ONLY in this valid JSON format, without any explanations or markdown:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }},
  ...
]
"""

    for model_name in MODELS_TO_TRY:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                output_text = response.text.strip()
                
                print(f"\n🔥 RAW GEMINI RESPONSE ({model_name}) 🔥\n", output_text)

                # Remove any markdown formatting if present
                if output_text.startswith("```json"):
                    output_text = output_text.replace("```json", "").replace("```", "").strip()
                elif output_text.startswith("```"):
                    output_text = output_text.replace("```", "").strip()

                panel_data = json.loads(output_text)

                # Additional structure validation
                if not isinstance(panel_data, list):
                    raise ValueError("Gemini response is not a list.")

                for panel in panel_data:
                    if not isinstance(panel, dict) or not all(key in panel for key in ("panel", "title", "scene_description", "image_prompt")):
                        raise ValueError(f"Invalid panel format or missing keys: {panel}")

                return panel_data

            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error on {model_name}:", e)
                print(f"❌ Full Text Received:\n", output_text)
                if attempt == 2:
                    return [{"error": f"JSON parsing failed: {str(e)}"}]
            except Exception as e:
                if "503" in str(e) or "404" in str(e):
                    time.sleep(2 * (attempt + 1))
                    continue
                print(f"❌ Unexpected Error on {model_name}:", e)
                if attempt == 2:
                    return [{"error": f"Generation failed: {str(e)}"}]

    return [{"error": "All Gemini endpoints are currently busy or unavailable."}]
