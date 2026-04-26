import pyttsx3
from pathlib import Path

# Save to the uploads folder where the app expects it
output_dir = Path("uploads")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "test_dental_case.wav"

text = """
The patient might have sensitivity but I'm not sure if it's tooth 12 or 22.
"""

# Use pyttsx3 - no FFmpeg needed, no internet needed
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed
engine.save_to_file(text, str(output_file))
engine.runAndWait()

print(f"✅ Audio file generated: {output_file}")
print(f"✅ Full path: {output_file.absolute()}")
