from pathlib import Path


file_path = Path("data/civic_services.txt")

text = file_path.read_text(encoding="utf-8")

print(text)