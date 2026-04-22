#!/usr/bin/env python3
"""Generate an image using Google AI Studio (Gemini)."""

import argparse
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

SKILL_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(SKILL_ROOT / ".env")

DEFAULT_MODEL_ID = os.environ.get(
    "GOOGLE_AI_STUDIO_MODEL", "gemini-3-pro-image-preview"
)
FALLBACK_MODEL_ID = "gemini-3.1-flash-image-preview"
MAX_RETRIES = 3
BASE_DELAY_S = 2.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an image from a text prompt using Gemini."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument(
        "--prompt", help="The full text prompt for image generation"
    )
    prompt_group.add_argument(
        "--prompt-file", help="Path to a UTF-8 text file containing the prompt"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_ID,
        help=(
            "Preferred Gemini model ID. Defaults to gemini-3-pro-image-preview "
            "or GOOGLE_AI_STUDIO_MODEL when set."
        ),
    )
    parser.add_argument(
        "--output", required=True, help="Output file path (extension auto-corrected to match actual format)"
    )
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    else:
        prompt = args.prompt.strip()

    if not prompt:
        raise ValueError("Prompt is empty")

    return prompt


def is_retryable_error(message: str) -> bool:
    return any(
        keyword in message
        for keyword in ("rate", "429", "quota", "500", "503", "internal")
    )


def is_model_unavailable(message: str) -> bool:
    return any(
        keyword in message
        for keyword in (
            "model",
            "not found",
            "unsupported",
            "permission",
            "access denied",
            "not available",
        )
    )


def _detect_ext_from_bytes(data: bytes) -> str:
    """Detect image format from magic bytes and return the file extension."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:2] == b"\xff\xd8":
        return ".jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return ".png"  # safe default


def extract_image_data(
    response: types.GenerateContentResponse,
) -> tuple[bytes, str]:
    """Return (raw_bytes, file_extension) for the first image part."""
    for part in response.parts:
        if part.inline_data is not None:
            data = part.inline_data.data
            # Prefer magic-byte detection over declared mime_type since
            # the API sometimes declares the wrong content type.
            ext = _detect_ext_from_bytes(data)
            return data, ext

    raise RuntimeError(
        "No image data found in response. The model may have returned text only."
    )


def generate_image(api_key: str, prompt: str, requested_model: str) -> tuple[bytes, str]:
    """Call Gemini image generation with retry logic and model fallback.

    Returns (image_bytes, file_extension) where extension includes the dot.
    """
    client = genai.Client(api_key=api_key)
    last_error: Exception | None = None

    model_candidates = [requested_model]
    if requested_model != FALLBACK_MODEL_ID:
        model_candidates.append(FALLBACK_MODEL_ID)

    for model_id in model_candidates:
        should_try_next_model = False

        for attempt in range(MAX_RETRIES):
            if attempt > 0:
                delay = BASE_DELAY_S * (2 ** (attempt - 1))
                print(f"  Retry {attempt}/{MAX_RETRIES - 1} after {delay:.0f}s...")
                time.sleep(delay)

            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                    ),
                )
                return extract_image_data(response)

            except Exception as err:
                last_error = err
                message = str(err).lower()

                if is_model_unavailable(message) and model_id != FALLBACK_MODEL_ID:
                    print(
                        f"  Model {model_id} unavailable, falling back to {FALLBACK_MODEL_ID}..."
                    )
                    should_try_next_model = True
                    break

                if is_retryable_error(message):
                    print("  Transient API error, will retry...")
                    continue

                raise

        if should_try_next_model:
            continue

        break

    raise RuntimeError(
        f"Failed after trying available models. Last error: {last_error}"
    )


def main() -> None:
    args = parse_args()

    api_key = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")
    if not api_key:
        print(
            "Error: GOOGLE_AI_STUDIO_API_KEY not set.\n"
            "Copy .env.example to .env and add your API key.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        prompt = load_prompt(args)
    except Exception as err:
        print(f"Error loading prompt: {err}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating image...")
    print(f"  Output: {output_path}")
    print(f"  Requested model: {args.model}")
    print(f"  Prompt length: {len(prompt)} chars")

    try:
        image_data, ext = generate_image(api_key, prompt, args.model)
        # Use the actual image format extension instead of whatever the
        # caller specified, so the file extension always matches the content.
        output_path = output_path.with_suffix(ext)
        output_path.write_bytes(image_data)
        size_kb = len(image_data) / 1024
        print(f"  Saved: {output_path} ({size_kb:.1f} KB)")
    except Exception as err:
        print(f"  FAILED: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
