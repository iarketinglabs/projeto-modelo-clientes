#!/usr/bin/env python3
"""
Quick validation script for skills - validates frontmatter, structure, and progressive disclosure.

Usage:
    python quick_validate.py <skill_directory> [--strict]

Strict mode additionally warns if:
    - SKILL.md exceeds 500 lines
    - No references/ directory exists when SKILL.md > 300 lines
    - references/ contains files but SKILL.md never mentions them
"""

import sys
import os
import re
import yaml
from pathlib import Path

# Allowed frontmatter properties
ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}


def validate_frontmatter(content: str) -> tuple[bool, str]:
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Frontmatter is valid!"


def validate_structure(skill_path: Path, content: str, strict: bool) -> tuple[bool, list[str]]:
    warnings = []
    lines = content.splitlines()
    line_count = len(lines)

    # Check for progressive disclosure best practices
    has_references_dir = (skill_path / 'references').exists() and any((skill_path / 'references').iterdir())
    has_scripts_dir = (skill_path / 'scripts').exists() and any((skill_path / 'scripts').iterdir())
    has_assets_dir = (skill_path / 'assets').exists() and any((skill_path / 'assets').iterdir())

    # Check if SKILL.md mentions references/
    mentions_references = 'references/' in content or 'Read `references/' in content
    mentions_scripts = 'scripts/' in content

    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines (recommended max: 500). Consider moving content to references/.")
        if strict and not has_references_dir:
            warnings.append("SKILL.md is very long but no references/ directory found. Consider using progressive disclosure.")

    if line_count > 300 and not has_references_dir:
        warnings.append("SKILL.md exceeds 300 lines but has no references/ directory. Consider extracting templates/guides to references/.")

    if has_references_dir and not mentions_references:
        warnings.append("references/ directory exists but SKILL.md never mentions it. Add pointers so the agent knows when to load them.")

    if has_scripts_dir and not mentions_scripts:
        warnings.append("scripts/ directory exists but SKILL.md never mentions it. Tell the agent when to use bundled scripts.")

    # Check for anti-patterns
    subjective_terms = ["rápido", "rápida", "lento", "lenta", "fácil", "intuitivo", "intuitiva", "escalável", "eficiente"]
    content_lower = content.lower()
    found_subjective = [t for t in subjective_terms if t in content_lower]
    if found_subjective:
        warnings.append(f"Potentially subjective terms found in SKILL.md: {', '.join(found_subjective)}. Consider quantifying them.")

    return True, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <skill_directory> [--strict]")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    strict = '--strict' in sys.argv

    if not skill_path.exists():
        print(f"[ERROR] Directory not found: {skill_path}")
        sys.exit(1)

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}")
        sys.exit(1)

    content = skill_md.read_text(encoding='utf-8')

    print(f"Validating skill: {skill_path.name}")
    print("=" * 50)

    # Frontmatter validation
    valid, msg = validate_frontmatter(content)
    status = "[OK]" if valid else "[FAIL]"
    print(f"{status} Frontmatter: {msg}")

    if not valid:
        sys.exit(1)

    # Structure validation
    _, warnings = validate_structure(skill_path, content, strict)
    if warnings:
        print("\n[WARN] Warnings:")
        for w in warnings:
            print(f"   - {w}")
    else:
        print("\n[OK] Structure checks passed with no warnings.")

    if warnings and strict:
        print("\n[EXIT] Strict mode: warnings treated as failures.")
        sys.exit(1)

    print("\n[DONE] Skill passed validation!")
    sys.exit(0)


if __name__ == "__main__":
    main()
