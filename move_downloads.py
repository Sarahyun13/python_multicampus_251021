import os
import shutil
from pathlib import Path

DOWNLOADS = r"C:\Users\student\Downloads"

# 확장자별 대상 폴더 (Downloads 폴더 내에 생성)
RULES = {
    "images": (".jpg", ".jpeg"),
    "data": (".csv", ".xlsx"),
    "docs": (".txt", ".doc", ".pdf"),
    "archive": (".zip",),
}

def ensure_dirs(base: str, folders):
    for name in folders:
        path = os.path.join(base, name)
        os.makedirs(path, exist_ok=True)

def find_target_folder(ext: str):
    for folder, exts in RULES.items():
        if ext.lower() in exts:
            return folder
    return None

def unique_dest(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 1
    while True:
        candidate = path.with_name(f"{stem} ({i}){suffix}")
        if not candidate.exists():
            return candidate
        i += 1

def organize_downloads():
    base = Path(DOWNLOADS)
    if not base.exists():
        print(f"다운로드 폴더가 없습니다: {DOWNLOADS}")
        return

    ensure_dirs(DOWNLOADS, RULES.keys())

    for entry in base.iterdir():
        if entry.is_dir():
            # 대상 폴더들 자체는 건너뜀
            if entry.name in RULES:
                continue
            else:
                continue
        ext = entry.suffix.lower()
        target_folder = find_target_folder(ext)
        if not target_folder:
            continue
        dest_dir = base / target_folder
        dest_path = dest_dir / entry.name
        dest_path = unique_dest(dest_path)
        try:
            shutil.move(str(entry), str(dest_path))
            print(f"이동: {entry.name} -> {dest_dir}\\{dest_path.name}")
        except Exception as e:
            print(f"실패: {entry.name} ({e})")

if __name__ == "__main__":
    organize_downloads()