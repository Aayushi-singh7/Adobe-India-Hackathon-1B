import os
import json
from utils.extractor import extract_pdf_sections
from utils.matcher import match_sections

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
PERSONA_FILE = os.path.join(INPUT_DIR, "persona.txt")

def main():
    # Step 1: Load persona JTBD
    if not os.path.exists(PERSONA_FILE):
        raise FileNotFoundError("Missing persona.txt in input directory")
    
    with open(PERSONA_FILE, "r", encoding="utf-8") as f:
        jtbd = f.read().strip()
    
    if not jtbd:
        raise ValueError("JTBD must be a non-empty string")

    # Step 2: Loop over PDF files
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)

            # Step 3: Extract headings/text
            content_sections = extract_pdf_sections(pdf_path)

            # Step 4: Match against JTBD
            best_matches = match_sections(jtbd, content_sections)

            # Step 5: Write output JSON
            output = {
                "persona": jtbd,
                "matches": best_matches
            }

            out_file = os.path.splitext(filename)[0] + ".json"
            with open(os.path.join(OUTPUT_DIR, out_file), "w", encoding="utf-8") as out_f:
                json.dump(output, out_f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
