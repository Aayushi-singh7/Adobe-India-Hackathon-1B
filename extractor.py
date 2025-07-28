import fitz  # PyMuPDF
from collections import defaultdict, Counter

# Optional toggle
USE_BOLD = True

def is_bold_font(font_name: str) -> bool:
    return any(kw in font_name.lower() for kw in ["bold", "black", "demi"])

def extract_pdf_structure(pdf_path):
    doc = fitz.open(pdf_path)
    blocks_per_page = []
    font_stats = Counter()

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_blocks = []

        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                font_sizes = []
                font_names = []
                bold = False

                for span in line["spans"]:
                    text = span.get("text", "").strip()
                    if not text:
                        continue

                    size = span["size"]
                    font = span["font"]
                    if USE_BOLD and is_bold_font(font):
                        bold = True

                    line_text += text + " "
                    font_sizes.append(size)
                    font_names.append(font)
                    font_stats[size] += 1

                if line_text.strip():
                    avg_size = round(sum(font_sizes) / len(font_sizes), 2)
                    block_info = {
                        "text": line_text.strip(),
                        "font_size": avg_size,
                        "font_name": font_names[0] if font_names else "",
                        "is_bold": bold,
                        "page": page_num
                    }
                    page_blocks.append(block_info)

        blocks_per_page.extend(page_blocks)

    # Determine heading levels based on most frequent font sizes
    common_fonts = font_stats.most_common()
    if len(common_fonts) < 3:
        raise ValueError("PDF does not contain enough font variety for heading detection.")

    body_font = common_fonts[0][0]
    heading_fonts = sorted([fs for fs, _ in font_stats.items() if fs > body_font], reverse=True)
    
    if len(heading_fonts) < 1:
        heading_fonts = [body_font + 1]  # Fallback if headings not obvious

    # Assign heading levels
    heading_levels = {}
    if len(heading_fonts) >= 3:
        heading_levels = {
            heading_fonts[0]: "H1",
            heading_fonts[1]: "H2",
            heading_fonts[2]: "H3"
        }
    elif len(heading_fonts) == 2:
        heading_levels = {
            heading_fonts[0]: "H1",
            heading_fonts[1]: "H2"
        }
    elif len(heading_fonts) == 1:
        heading_levels = {
            heading_fonts[0]: "H1"
        }

    outline = []
    current_heading = None

    for block in blocks_per_page:
        size = block["font_size"]
        text = block["text"]
        page = block["page"]
        is_heading = False

        if size in heading_levels:
            level = heading_levels[size]
            current_heading = {
                "level": level,
                "text": text,
                "page": page,
                "content": ""
            }
            outline.append(current_heading)
            is_heading = True

        elif current_heading and not is_heading:
            # Append to current heading's content
            current_heading["content"] += " " + text

    return outline
