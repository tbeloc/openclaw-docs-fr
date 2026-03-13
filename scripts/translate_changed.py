import os
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

EN = Path("docs/en")
FR = Path("docs/fr")


def translate(text):
    prompt = """
Translate this technical documentation to French.

Rules:
- Keep markdown/MDX structure identical
- Do not translate code blocks
- Do not modify links or URLs
- Do not change filenames, anchors, imports or frontmatter keys
- Return ONLY the translated content
"""

    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        temperature=0,
        messages=[{
            "role": "user",
            "content": prompt + "\n\n" + text
        }]
    )

    parts = []

    for block in r.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)

    return "".join(parts).strip()


for root, dirs, files in os.walk(EN):
    for file in files:

        if not file.endswith((".md", ".mdx")):
            continue

        src = Path(root) / file
        rel = src.relative_to(EN)
        dst = FR / rel

        dst.parent.mkdir(parents=True, exist_ok=True)

        # IMPORTANT : ne pas retraduire
        if dst.exists():
            print(f"skip existing: {rel}")
            continue

        print(f"translating: {rel}")

        text = src.read_text(encoding="utf-8")

        fr = translate(text)

        dst.write_text(fr + "\n", encoding="utf-8")

        print(f"translated: {rel}")
