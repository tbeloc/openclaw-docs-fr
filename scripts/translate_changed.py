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


def translate(text):
    prompt = """
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

    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16000,
        temperature=0,
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


def check_mdx_balance(text):
    """
    Check that every MDX opening tag has a matching closing tag.
    Returns a list of unbalanced tag names, or an empty list if balanced.
    """
    opening = re.findall(r'<([A-Z][a-zA-Z]*)\b', text)
    closing = re.findall(r'</([A-Z][a-zA-Z]*)\b', text)

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


MAX_RETRIES = 2

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

        # Check if source has MDX tags to validate
        src_tags = re.findall(r'<([A-Z][a-zA-Z]*)\b', text)
        has_mdx = len(src_tags) > 0

        fr = translate(text)

        # Validate MDX balance if source had MDX components
        if has_mdx:
            for attempt in range(MAX_RETRIES):
                issues = check_mdx_balance(fr)
                if not issues:
                    break
                print(f"  WARNING: unbalanced MDX tags: {', '.join(issues)} — retrying ({attempt + 1}/{MAX_RETRIES})", flush=True)
                fr = translate(text)
            else:
                issues = check_mdx_balance(fr)
                if issues:
                    print(f"  SKIPPING {rel}: still unbalanced after {MAX_RETRIES} retries: {', '.join(issues)}", flush=True)
                    continue

        dst.write_text(fr + "\n", encoding="utf-8")

        print(f"translated: {rel}", flush=True)
