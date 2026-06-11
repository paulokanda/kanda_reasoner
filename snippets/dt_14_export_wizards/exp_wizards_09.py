# export_wizards_09/exp_wizards_09.py

import datetime
from pathlib import Path
from shutil import copyfile

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def export_bundle(trace_file, spectrogram_image, annotations_file, tag="session"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_folder = EXPORT_DIR / f"{tag}_{timestamp}"
    session_folder.mkdir()

    files = {
        "trace.json": trace_file,
        "spectrogram.png": spectrogram_image,
        "annotations.txt": annotations_file,
    }

    for name, src in files.items():
        src_path = Path(src)
        if not src_path.exists():
            print(f"❌ Missing file: {src_path}")
            continue
        dst_path = session_folder / name
        copyfile(src_path, dst_path)
        print(f"✅ Exported: {dst_path}")

    print(f"📦 Export complete. Bundle located at: {session_folder.resolve()}")

if __name__ == "__main__":
    print("📂 Enter path to trace JSON file:")
    trace = input("> ").strip()
    print("🖼️  Enter path to spectrogram image (PNG):")
    spectrogram = input("> ").strip()
    print("📝 Enter path to annotations file:")
    annotations = input("> ").strip()

    export_bundle(trace, spectrogram, annotations)
