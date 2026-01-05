from pathlib import Path
import shutil


def organize_files(directory: Path, dry_run: bool = True):
    if not directory.exists() or not directory.is_dir():
        print("Invalid directory.")
        return

    files = [f for f in directory.iterdir() if f.is_file()]

    if not files:
        print("No files to organize.")
        return

    for file in files:
        extension = file.suffix.lower().lstrip(".")

        if not extension:
            extension = "no_extension"

        target_dir = directory / extension

        if dry_run:
            print(f"[DRY RUN] Move {file.name} -> {target_dir}/")
        else:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(file), target_dir / file.name)

    if dry_run:
        print("\nDry run complete. No files were moved.")
    else:
        print("\nFiles organized successfully.")


def main():
    path_input = input("Enter directory path: ").strip()
    directory = Path(path_input)

    choice = input("Dry run? (y/n): ").strip().lower()
    dry_run = choice != "n"

    organize_files(directory, dry_run=dry_run)


if __name__ == "__main__":
    main()
