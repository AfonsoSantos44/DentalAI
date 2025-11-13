from gtts import gTTS

text = """
The patient reports sensitivity on tooth eleven and twelve.
There is mild gingivitis.
Scaling was performed today.
Recommend a follow up appointment in thirty days.
"""

tts = gTTS(text=text, lang="en")
tts.save("test_dental_case.mp3")

print("✅ Audio file generated: test_dental_case.mp3")
