# Adobe Hackathon 2025 – Round 1B

## Objective
Match persona job-to-be-done (JTBD) with relevant sections in a set of PDFs.

## Input
- `input/*.pdf`: Set of documents
- `input/persona.json`: JSON file with fields `"persona"` and `"jtbd"`

## Output
- `output/matched_output.json`: Structured mapping of relevant sections per PDF

## How to Run (Offline)
```bash
docker build --platform linux/amd64 -t document-matcher:offline .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none document-matcher:offline
