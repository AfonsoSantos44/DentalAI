import requests
from pathlib import Path

# Test audio file path
audio_file = Path("uploads/test_dental_case.mp3")

if not audio_file.exists():
    print(f"❌ Audio file not found: {audio_file.absolute()}")
    exit(1)

print(f"✓ Found audio file: {audio_file.absolute()}")
print(f"✓ File size: {audio_file.stat().st_size} bytes")

# Post to backend
url = "http://127.0.0.1:8001/audio/process_full"

print(f"\n📤 Posting to {url}...")

try:
    with open(audio_file, "rb") as f:
        files = {"file": (audio_file.name, f, "audio/mpeg")}
        response = requests.post(url, files=files, timeout=60)
    
    print(f"📥 Response status: {response.status_code}")
    print(f"📥 Response body:\n{response.text}")
    
    if response.status_code == 200:
        print("\n✅ Success!")
        print(response.json())
    else:
        print(f"\n❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Request failed: {e}")
