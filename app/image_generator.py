import os
import re
import torch
from diffusers import StableDiffusionPipeline

# Suppress Hugging Face symlinks warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Initialize local Stable Diffusion pipeline on CPU
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe = pipe.to("cpu")

def sanitize_filename(prompt: str) -> str:
    clean = re.sub(r'[^\w\s-]', '', prompt).strip().lower()
    clean = re.sub(r'[-\s]+', '_', clean)[:30]
    return f"{clean}.png"

def generate_image(prompt, filename=None):
    if not filename:
        filename = sanitize_filename(prompt)

    image = pipe(prompt).images[0]
    path = f"static/panels/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)
    return path
