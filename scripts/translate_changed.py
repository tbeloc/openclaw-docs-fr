import os
from pathlib import Path
from anthropic import Anthropic

# connexion API
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

EN = Path("docs/en")
FR = Path("docs/fr")

# fichier test
TEST_FILE = EN / "index.md"


def translate(text):
    prompt = """
Translate this technical documentation to French.

Rules:
- Keep markdown structure identical
- Do not translate code blocks
- Do not modify links or URLs
- Do not change filenames or anchors
- Do not change frontmatter keys
- Return ONLY the translated content
"""

    r = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt + "\n\n" + text
            }
        ]
    )

    parts = []

    for block in r.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)

    return "".join(parts).strip()


# vérifie que le fichier existe
if not TEST_FILE.exists():
    raise FileNotFoundError(f"Test file not found: {TEST_FILE}")

rel = TEST_FILE.relative_to(EN)
dst = FR / rel

dst.parent.mkdir(parents=True, exist_ok=True)

print(f"translating test file: {rel}")

text = TEST_FILE.read_text(encoding="utf-8")

fr = translate(text)

dst.write_text(fr + "\n", encoding="utf-8")

print(f"translated: {rel}")
