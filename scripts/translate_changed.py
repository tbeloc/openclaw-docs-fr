import os
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

EN = Path("docs/en")
FR = Path("docs/fr")

def translate(text):

    prompt = "Translate this technical documentation to French. Keep markdown and code blocks unchanged."

    r = client.messages.create(
        model="claude-3-5-sonnet",
        max_tokens=8000,
        messages=[{
            "role": "user",
            "content": prompt + "\n\n" + text
        }]
    )

    return r.content[0].text


for root, dirs, files in os.walk(EN):

    for file in files:

        if not file.endswith(".md") and not file.endswith(".mdx"):
            continue

        src = Path(root) / file

        rel = src.relative_to(EN)

        dst = FR / rel

        dst.parent.mkdir(parents=True, exist_ok=True)

        text = src.read_text()

        fr = translate(text)

        dst.write_text(fr)

        print("translated", rel)
