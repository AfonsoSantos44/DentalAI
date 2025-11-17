import os
import uuid
from pathlib import Path
from typing import Optional

from app.core.config.settings import get_settings

settings = get_settings()

VALID_AUDIO_EXTENSIONS = {"wav", "mp3", "m4a", "mpeg"}


def _resolve_save_directory(save_path: Optional[str]) -> Path:
    """Resolve the target directory for uploads based on provided path.

    - ``None`` or empty paths default to ``settings.upload_folder``.
    - The special value ``"temp"`` uses ``settings.temp_audio_folder``.
    - Relative paths are nested under ``settings.upload_folder``.
    - Absolute paths are used as-is.
    """

    if not save_path:
        directory = Path(settings.upload_folder)
    elif save_path == "temp":
        directory = Path(settings.temp_audio_folder)
    elif os.path.isabs(save_path):
        directory = Path(save_path)
    else:
        directory = Path(settings.upload_folder) / save_path

    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _extract_normalized_extension(filename: str) -> str:
    """Return a validated, lowercase extension from an uploaded filename."""

    cleaned_name = os.path.basename(filename or "").strip()
    stem, ext = os.path.splitext(cleaned_name)

    if not stem or not ext:
        raise ValueError("Uploaded file must include a non-empty name and extension.")

    normalized_ext = ext.lstrip(".").lower()
    if normalized_ext not in VALID_AUDIO_EXTENSIONS:
        raise ValueError("Unsupported file extension for upload.")

    return normalized_ext


def save_uploaded_file(uploaded_file, save_path: Optional[str] = None):
    upload_dir = _resolve_save_directory(save_path)
    ext = _extract_normalized_extension(uploaded_file.filename)
    unique_filename = f"{uuid.uuid4()}.{ext}"

    filepath = upload_dir / unique_filename

    with filepath.open("wb") as f:
        f.write(uploaded_file.file.read())

    return str(filepath)


def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
