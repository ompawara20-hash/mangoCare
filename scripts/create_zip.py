"""
MangoCare AI Archive Creator and Verification Script
Packages the project into MangoCare-AI.zip, verifies archive integrity, and computes SHA-256
"""
import os
import sys
import zipfile
import hashlib
import tempfile
from pathlib import Path

# Exclusion rules
EXCLUDE_DIRS = {
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist-ssr"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store",
}

EXCLUDE_FILES = {
    ".env",
    ".env.local",
    "mangocare.db",
    "test_mangocare.db",
    "mangocare.db-journal",
    "mangocare.db-wal",
    "mangocare.db-shm"
}

# Model weights are excluded from ZIP to ensure a lightweight, fast-extracting package;
# users obtain them via `python backend/scripts/download_model.py`
EXCLUDE_WEIGHT_EXTENSIONS = {
    ".safetensors",
    ".pth",
    ".bin"
}


def should_exclude(rel_path: Path) -> bool:
    parts = rel_path.parts
    # Check directory names
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True

    # Check filename
    filename = rel_path.name
    if filename in EXCLUDE_FILES:
        return True

    # Check extension
    suffix = rel_path.suffix.lower()
    if suffix in EXCLUDE_EXTENSIONS or suffix in EXCLUDE_WEIGHT_EXTENSIONS:
        return True

    # Check reports pdf (keep .gitkeep only)
    if "reports" in parts and suffix == ".pdf":
        return True

    # Check data db files (keep .gitkeep only)
    if "data" in parts and suffix in (".db", ".sqlite", ".sqlite3"):
        return True

    return False


def create_archive():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    workspace_dir = project_root.parent
    output_zip = workspace_dir / "MangoCare-AI.zip"

    print("=" * 65)
    print(" MangoCare AI - Package Builder & Verification")
    print("=" * 65)
    print(f"Source Directory: {project_root}")
    print(f"Output ZIP:       {output_zip}")

    total_files = 0
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as zf:
        for root, dirs, files in os.walk(project_root):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(project_root)

                if should_exclude(rel_path):
                    continue

                archive_arcname = Path("MangoCare-AI") / rel_path
                zf.write(full_path, arcname=str(archive_arcname))
                total_files += 1

    file_size_bytes = output_zip.stat().st_size
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Compute SHA256
    sha256 = hashlib.sha256()
    with open(output_zip, "rb") as f:
        while chunk := f.read(1024 * 1024):
            sha256.update(chunk)
    checksum = sha256.hexdigest()

    print(f"\n[OK] Archive successfully generated!")
    print(f" - Absolute Path: {output_zip.resolve()}")
    print(f" - File Size:     {file_size_mb:.2f} MB ({file_size_bytes:,} bytes)")
    print(f" - Files Packed:  {total_files} files")
    print(f" - SHA-256:       {checksum}")

    # Verify opening archive
    print("\nVerifying archive integrity...")
    with zipfile.ZipFile(output_zip, "r") as zf:
        test_res = zf.testzip()
        if test_res is not None:
            raise RuntimeError(f"Corrupted file in archive: {test_res}")
        namelist = zf.namelist()
        print(f"[OK] Archive test passed: {len(namelist)} items readable.")

    # Test extraction into a clean temporary directory
    print("\nTesting extraction into clean sandbox...")
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(output_zip, "r") as zf:
            zf.extractall(temp_dir)
        extracted_root = Path(temp_dir) / "MangoCare-AI"

        # Verify key deliverables exist
        critical_files = [
            extracted_root / "README.md",
            extracted_root / "MODEL_CARD.md",
            extracted_root / "backend" / "requirements.txt",
            extracted_root / "backend" / "app" / "main.py",
            extracted_root / "backend" / "app" / "ml" / "mango_classifier.py",
            extracted_root / "backend" / "app" / "ml" / "mango_validator.py",
            extracted_root / "backend" / "app" / "knowledge" / "disease_info.json",
            extracted_root / "frontend" / "package.json",
            extracted_root / "frontend" / "src" / "App.tsx",
            extracted_root / "frontend" / "dist" / "index.html",
            extracted_root / "docker-compose.yml",
            extracted_root / "scripts" / "setup_windows.ps1",
            extracted_root / "scripts" / "run_windows.ps1",
        ]

        for cf in critical_files:
            if not cf.is_file():
                raise FileNotFoundError(f"Missing critical deliverable in archive: {cf}")

        print(f"[OK] Clean sandbox extraction test passed: All critical deliverables verified.")

    print("\n" + "=" * 65)
    print(" PACKAGING AND VERIFICATION COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    return output_zip, checksum

if __name__ == "__main__":
    create_archive()
