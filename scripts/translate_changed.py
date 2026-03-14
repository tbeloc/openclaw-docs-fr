import os
import re
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

EN = Path("docs/en")
FR = Path("docs/en/fr")

# Subdirectories to skip (other languages living inside docs/en/)
SKIP_DIRS = {"zh-CN", "ja-JP", "fr"}

# MDX self-closing tags that don't need a closing counterpart
SELF_CLOSING_TAGS = {"img", "br", "hr", "Frame", "Icon"}

# Rough char threshold for chunking (~3000 tokens input → safe 16k output)
CHUNK_CHAR_LIMIT = 12000

TRANSLATE_PROMPT = """
Translate this technical documentation to French.

Rules:
- Keep markdown / MDX structure identical (all opening and closing tags MUST be preserved)
- Do not translate code blocks
- Do not modify links or URLs
- Do not change filenames, anchors, imports or frontmatter keys
- Preserve ALL MDX/JSX components exactly (<Tabs>, <Tab>, <Steps>, <Step>, <Accordion>, <AccordionGroup>, <Note>, <Tip>, <Warning>, <Info>, <Card>, <CardGroup>, <CODE> etc.)
- Every opening tag MUST have its matching closing tag
- Return ONLY the translated content, complete and untruncated
"""


def translate(text):
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": TRANSLATE_PROMPT + "\n\n" + text
            }
        ]
    )

    parts = []
    for block in r.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)

    return "".join(parts).strip()


def split_into_chunks(text):
    """
    Split a markdown document into chunks at H2 (##) boundaries.
    The frontmatter (---...---) stays attached to the first chunk.
    Each chunk stays under CHUNK_CHAR_LIMIT when possible.
    """
    # Separate frontmatter
    frontmatter = ""
    body = text
    fm_match = re.match(r'^(---\n.*?\n---\n)(.*)', text, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = fm_match.group(2)

    # Split on H2 headings (keep the heading with the section that follows)
    sections = re.split(r'(?=\n## )', body)

    chunks = []
    current = frontmatter

    for section in sections:
        # If adding this section would exceed the limit and we already have content
        if len(current) + len(section) > CHUNK_CHAR_LIMIT and current.strip():
            chunks.append(current)
            current = section
        else:
            current += section

    if current.strip():
        chunks.append(current)

    return chunks


def strip_code_blocks(text):
    """Remove fenced code blocks and inline code so tags inside them are ignored."""
    # Remove fenced code blocks (```...```)
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code (`...`)
    text = re.sub(r'`[^`]+`', '', text)
    return text


def check_mdx_balance(text):
    """
    Check that every MDX opening tag has a matching closing tag.
    Ignores tags inside code blocks and inline code.
    Returns a list of unbalanced tag names, or an empty list if balanced.
    """
    cleaned = strip_code_blocks(text)
    opening = re.findall(r'<([A-Z][a-zA-Z]*)\b', cleaned)
    closing = re.findall(r'</([A-Z][a-zA-Z]*)\b', cleaned)

    open_counts = {}
    for tag in opening:
        if tag not in SELF_CLOSING_TAGS:
            open_counts[tag] = open_counts.get(tag, 0) + 1

    close_counts = {}
    for tag in closing:
        close_counts[tag] = close_counts.get(tag, 0) + 1

    unbalanced = []
    all_tags = set(list(open_counts.keys()) + list(close_counts.keys()))
    for tag in all_tags:
        o = open_counts.get(tag, 0)
        c = close_counts.get(tag, 0)
        if o != c:
            unbalanced.append(f"{tag} (open={o}, close={c})")

    return unbalanced


def translate_with_validation(text):
    """Translate text and validate MDX balance. Retries up to 2 times."""
    src_tags = re.findall(r'<([A-Z][a-zA-Z]*)\b', text)
    has_mdx = len(src_tags) > 0

    for attempt in range(3):
        fr = translate(text)

        if not has_mdx:
            return fr

        issues = check_mdx_balance(fr)
        if not issues:
            return fr

        if attempt < 2:
            print(f"    unbalanced MDX: {', '.join(issues)} — retrying ({attempt + 1}/2)", flush=True)

    return None  # still broken after retries


for root, dirs, files in os.walk(EN):
    # Prune language subdirectories so os.walk doesn't descend into them
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

    for file in files:
        if not file.endswith((".md", ".mdx")):
            continue

        src = Path(root) / file
        rel = src.relative_to(EN)
        dst = FR / rel

        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists():
            print(f"skip existing: {rel}", flush=True)
            continue

        print(f"translating: {rel}", flush=True)

        text = src.read_text(encoding="utf-8")

        # Decide: chunk large files, translate small ones directly
        if len(text) > CHUNK_CHAR_LIMIT:
            chunks = split_into_chunks(text)
            print(f"  large file ({len(text)} chars) → split into {len(chunks)} chunks", flush=True)

            translated_chunks = []
            failed = False
            for i, chunk in enumerate(chunks):
                print(f"  chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)", flush=True)
                result = translate_with_validation(chunk)
                if result is None:
                    print(f"  SKIPPING {rel}: chunk {i + 1} has unbalanced MDX after retries", flush=True)
                    failed = True
                    break
                translated_chunks.append(result)

            if failed:
                continue

            fr = "\n\n".join(translated_chunks)
        else:
            fr = translate_with_validation(text)
            if fr is None:
                print(f"  SKIPPING {rel}: unbalanced MDX after retries", flush=True)
                continue

        dst.write_text(fr + "\n", encoding="utf-8")

        print(f"translated: {rel}", flush=True)
