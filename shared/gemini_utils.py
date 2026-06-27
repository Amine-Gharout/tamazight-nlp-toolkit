"""
Shared Gemini utility module for OCR and ASR pipelines.

Provides common logic for:
- API key loading from environment
- File upload and content generation
- Result saving

Usage:
    from shared.gemini_utils import GeminiProcessor

    processor = GeminiProcessor()
    processor.process_directory(
        input_dir="doc",
        output_dir="outputs",
        system_prompt="...",
        file_type="image",  # or "audio"
    )
"""

import google.generativeai as genai
import os
import sys
import pathlib


class GeminiProcessor:
    """Handles Gemini-based batch processing (OCR or transcription)."""

    def __init__(self, model_name: str = "gemini-2.5-pro"):
        """Initialize with API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ ERROR: GEMINI_API_KEY environment variable not set.")
            print("   Set it with: export GEMINI_API_KEY='your-key-here'")
            print("   Or create a .env file with: GEMINI_API_KEY=your-key-here")
            sys.exit(1)

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def process_file(self, filepath: str, system_prompt: str) -> str:
        """
        Upload a file to Gemini and generate content using the system prompt.

        Args:
            filepath: Path to the input file (image or audio).
            system_prompt: System instruction for the model.

        Returns:
            Response text from the model.
        """
        uploaded_file = genai.upload_file(pathlib.Path(filepath))
        response = self.model.generate_content([system_prompt, uploaded_file])
        return response.text

    def process_directory(
        self,
        input_dir: str,
        output_dir: str,
        system_prompt: str,
        extensions: tuple | None = None,
    ) -> int:
        """
        Process all files in a directory through Gemini.

        Args:
            input_dir: Directory containing input files.
            output_dir: Directory to save results (created if needed).
            system_prompt: System instruction for the model.
            extensions: Optional tuple of valid extensions (e.g. ('.jpg', '.png')).

        Returns:
            Number of successfully processed files.
        """
        os.makedirs(output_dir, exist_ok=True)

        all_files = sorted(os.listdir(input_dir))
        files = [
            f for f in all_files
            if os.path.isfile(os.path.join(input_dir, f))
            and (extensions is None or os.path.splitext(f)[1].lower() in extensions)
        ]

        total = len(files)
        success = 0

        for i, file in enumerate(files, start=1):
            in_path = os.path.join(input_dir, file)
            stem = os.path.splitext(file)[0]
            out_path = os.path.join(output_dir, f"{stem}.md")

            print(f"  [{i}/{total}] Processing: {file}")

            try:
                text = self.process_file(in_path, system_prompt)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(f"{text}\n")
                print(f"    ✅ Saved to: {out_path}")
                success += 1
            except Exception as e:
                print(f"    ❌ Error: {e}")

        print(f"\n✅ Done! {success}/{total} files processed successfully.")
        return success
