"""
Inject the FR language entry into docs/en/docs.json.

Reads the EN navigation, deep-copies it, prefixes every page path
with 'fr/', translates tab and group names, and appends (or replaces)
the FR language block.  Run this AFTER rsync so upstream nav changes
are picked up automatically.
"""

import json
import copy
from pathlib import Path

DOCS_JSON = Path("docs/en/docs.json")
FR_DIR = Path("docs/en/fr")
PREFIX = "fr"

# ── Translation maps ────────────────────────────────────────────────
TAB_NAMES = {
    "Get started": "Démarrage",
    "Install": "Installation",
    "Channels": "Canaux",
    "Agents": "Agents",
    "Tools": "Outils",
    "Models": "Modèles",
    "Platforms": "Plateformes",
    "Gateway & Ops": "Passerelle & Ops",
    "Reference": "Référence",
    "Help": "Aide",
}

GROUP_NAMES = {
    "Home": "Accueil",
    "Overview": "Aperçu",
    "Core concepts": "Concepts clés",
    "First steps": "Premiers pas",
    "Guides": "Guides",
    "Package managers": "Gestionnaires de paquets",
    "Containers": "Conteneurs",
    "Build from source": "Compiler depuis les sources",
    "Migrate": "Migration",
    "Cloud hosting": "Hébergement cloud",
    "Messaging": "Messagerie",
    "Social": "Social",
    "Collaboration": "Collaboration",
    "Overview": "Aperçu",
    "Agent features": "Fonctionnalités des agents",
    "Multi-agent": "Multi-agent",
    "Coding agents": "Agents de code",
    "Custom agents": "Agents personnalisés",
    "Built-in tools": "Outils intégrés",
    "Nodes": "Nœuds",
    "Custom tools": "Outils personnalisés",
    "MCP": "MCP",
    "File tools": "Outils de fichiers",
    "Remote tools": "Outils distants",
    "Browser tools": "Outils de navigation",
    "Deprecated": "Obsolète",
    "Providers": "Fournisseurs",
    "Provider features": "Fonctionnalités des fournisseurs",
    "Local models": "Modèles locaux",
    "Special providers": "Fournisseurs spéciaux",
    "Desktop & mobile": "Bureau & mobile",
    "Self-hosted": "Auto-hébergé",
    "Gateway": "Passerelle",
    "Automation": "Automatisation",
    "Operations": "Opérations",
    "Observability": "Observabilité",
    "Configuration": "Configuration",
    "CLI": "CLI",
    "API": "API",
    "Specification": "Spécification",
    "Data": "Données",
    "Internal": "Interne",
    "Advanced": "Avancé",
    "Troubleshooting": "Dépannage",
    "FAQ": "FAQ",
    "Community": "Communauté",
    "Contributing": "Contribuer",
    "Resources": "Ressources",
    "Legal": "Légal",
    "Security": "Sécurité",
}


def fr_file_exists(page: str) -> bool:
    """Check whether the translated FR file exists on disk."""
    for ext in (".mdx", ".md"):
        if (FR_DIR / page).with_suffix(ext).exists():
            return True
    # Also check if the path already has an extension
    if (FR_DIR / page).exists():
        return True
    return False


def prefix_page(page: str) -> str:
    """Add the language prefix to a page path."""
    return f"{PREFIX}/{page}"


def prefix_pages(obj):
    """
    Recursively walk the navigation structure, prefix every page string
    with 'fr/', and drop pages whose FR file does not exist yet.
    """
    if isinstance(obj, str):
        if not fr_file_exists(obj):
            return None  # mark for removal
        return prefix_page(obj)
    if isinstance(obj, list):
        result = []
        for item in obj:
            transformed = prefix_pages(item)
            if transformed is not None:
                result.append(transformed)
        return result
    if isinstance(obj, dict):
        out = {}
        for key, val in obj.items():
            if key == "pages":
                out[key] = prefix_pages(val)
            elif key == "page":
                if isinstance(val, str) and not fr_file_exists(val):
                    return None  # drop the whole entry
                out[key] = prefix_page(val) if isinstance(val, str) else val
            elif key == "tab":
                out[key] = TAB_NAMES.get(val, val)
            elif key == "group":
                out[key] = GROUP_NAMES.get(val, val)
            elif key == "groups":
                out[key] = prefix_pages(val)
            else:
                out[key] = val
        # Drop groups with no pages left
        if "pages" in out and len(out["pages"]) == 0:
            return None
        return out
    return obj


def main():
    data = json.loads(DOCS_JSON.read_text("utf-8"))
    languages = data["navigation"]["languages"]

    # Find the EN entry
    en_entry = None
    for lang in languages:
        if lang.get("language") == "en":
            en_entry = lang
            break

    if en_entry is None:
        print("ERROR: no 'en' language entry found in docs.json")
        return

    # Deep-copy EN and transform into FR
    fr_entry = copy.deepcopy(en_entry)
    fr_entry["language"] = "fr"
    fr_entry["tabs"] = prefix_pages(fr_entry.get("tabs", []))

    # Drop tabs that ended up with no groups
    fr_entry["tabs"] = [
        t for t in fr_entry["tabs"]
        if t and t.get("groups")
    ]

    if not fr_entry["tabs"]:
        print("WARNING: no FR pages found, skipping injection")
        return

    # Remove existing FR entry if present, then append
    languages = [l for l in languages if l.get("language") != "fr"]
    languages.append(fr_entry)
    data["navigation"]["languages"] = languages

    DOCS_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Injected FR language entry ({len(fr_entry.get('tabs', []))} tabs)")


if __name__ == "__main__":
    main()
