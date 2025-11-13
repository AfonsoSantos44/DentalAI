import uuid
from app.config.settings import get_settings
import os

settings = get_settings()


def save_uploaded_file(uploaded_file, save_path="uploads"):
    os.makedirs(settings.upload_folder, exist_ok=True)

    ext = uploaded_file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(settings.upload_folder, unique_filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.file.read())

    return filepath

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)