from gtts import gTTS

text = """
"The patient might have sensitivity but I'm not sure if it's tooth 12 or 22."
"""

tts = gTTS(text=text, lang="en")
tts.save("test_dental_case.mp3")

print("✅ Audio file generated: test_dental_case.mp3")
