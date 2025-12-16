from __future__ import annotations

import re
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

from apps.autocare.schema.normalizer import camel_to_snake

M2M_RE = re.compile(r"#\s*M2M_JOIN_CANDIDATE:\s*(?P<a>\w+)\s*<->\s*(?P<b>\w+)\s*$")
CLASS_RE = re.compile(r"^class\s+(?P<cls>\w+)\s*\(", re.M)

# Minimal plural rules + overrides (fixes class -> classes)
PLURAL_OVERRIDES = {
    "class": "classes",
}


def pluralize(word: str) -> str:
    w = word.lower()
    if w in PLURAL_OVERRIDES:
        return PLURAL_OVERRIDES[w]
    if w.endswith("y") and len(w) > 1 and w[-2] not in "aeiou":
        return w[:-1] + "ies"
    if w.endswith(("s", "x", "z", "ch", "sh")):
        return w + "es"
    return w + "s"


def ensure_import_models(text: str) -> str:
    if re.search(r"^from django\.db import models\s*$", text, flags=re.M):
        return text
    # Put it at the top.
    return "from django.db import models\n\n" + text


def has_m2m_field(text: str, field_name: str, through_cls: str) -> bool:
    # crude but effective idempotency guard
    patt = re.compile(
        rf"^\s+{re.escape(field_name)}\s*=\s*models\.ManyToManyField\(\s*"
        rf"\"[^\"]+\"\s*,\s*through\s*=\s*\"{re.escape(through_cls)}\"",
        re.M,
    )
    return bool(patt.search(text))


def inject_m2m_field(text: str, *, field_name: str, to_model: str, through_cls: str, related_name: str) -> str:
    """
    Injects the M2M field into the *first* model class in the file,
    immediately before `class Meta:`. Idempotent guarded externally.
    """
    insert_block = (
        f"\n"
        f"    {field_name} = models.ManyToManyField(\n"
        f"        \"{to_model}\",\n"
        f"        through=\"{through_cls}\",\n"
        f"        related_name=\"{related_name}\",\n"
        f"    )\n"
    )

    # Insert before the first "class Meta:" inside the model
    idx = text.find("\n    class Meta:")
    if idx == -1:
        raise CommandError("Could not find 'class Meta:' in target model file to inject M2M field.")
    return text[:idx] + insert_block + text[idx:]


class Command(BaseCommand):
    help = "Promote M2M join candidates into ManyToManyField definitions (idempotent, deterministic)."

    def add_arguments(self, parser):
        parser.add_argument("--db", default="vcdb", help="Database name folder under apps/autocare/models (default: vcdb)")
        parser.add_argument("--models-dir", default=None, help="Override models directory (advanced)")

    def handle(self, *args, **opts):
        db = opts["db"]
        base_dir = Path(opts["models_dir"]) if opts["models_dir"] else Path(f"apps/autocare/models/{db}")

        if not base_dir.exists():
            raise CommandError(f"Models directory not found: {base_dir}")

        join_files = list(base_dir.glob("*.py"))
        if not join_files:
            raise CommandError(f"No model files found in {base_dir}")

        promoted = 0
        skipped = 0

        for jf in join_files:
            text = jf.read_text()

            m = M2M_RE.search(text)
            if not m:
                continue

            a = m.group("a")
            b = m.group("b")

            cls_m = CLASS_RE.search(text)
            if not cls_m:
                raise CommandError(f"Join model file {jf} has M2M_JOIN_CANDIDATE but no class definition found.")
            through_cls = cls_m.group("cls")

            # endpoint files are expected to be snake_case filenames
            a_file = base_dir / f"{camel_to_snake(a)}.py"
            b_file = base_dir / f"{camel_to_snake(b)}.py"

            if not a_file.exists() or not b_file.exists():
                raise CommandError(
                    f"M2M candidate {a} <-> {b} via {through_cls} but endpoint file missing: "
                    f"{a_file if not a_file.exists() else ''} {b_file if not b_file.exists() else ''}".strip()
                )

            # Inject on A: field name is plural of B (e.g., bed_configs)
            a_field = pluralize(camel_to_snake(b))
            a_related = pluralize(camel_to_snake(a))  # reverse accessor name on B instances

            # Inject on B: field name is plural of A (e.g., vehicles)
            b_field = pluralize(camel_to_snake(a))
            b_related = pluralize(camel_to_snake(b))

            # Apply A side
            a_text = ensure_import_models(a_file.read_text())
            if has_m2m_field(a_text, a_field, through_cls):
                skipped += 1
            else:
                a_text = inject_m2m_field(
                    a_text,
                    field_name=a_field,
                    to_model=b,
                    through_cls=through_cls,
                    related_name=a_related,
                )
                a_file.write_text(a_text)
                promoted += 1

            # Apply B side
            b_text = ensure_import_models(b_file.read_text())
            if has_m2m_field(b_text, b_field, through_cls):
                skipped += 1
            else:
                b_text = inject_m2m_field(
                    b_text,
                    field_name=b_field,
                    to_model=a,
                    through_cls=through_cls,
                    related_name=b_related,
                )
                b_file.write_text(b_text)
                promoted += 1

        self.stdout.write(self.style.SUCCESS(f"M2M promotion complete. Injected: {promoted}, Skipped (already present): {skipped}"))
