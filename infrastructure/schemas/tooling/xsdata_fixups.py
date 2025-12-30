from pathlib import Path
import re


REQUIRED_LIST = re.compile(
    r"""
    (?P<field>
        \w+\s*:\s*List\[.*?\]\s*=\s*field\(\n
        \s*default_factory=list,\n
        (?P<meta>.*?"min_occurs"\s*:\s*1,.*?)
        \n\s*\)
    )
    """,
    re.S | re.X,
)


def fix_required_lists(root: Path) -> int:
    count = 0
    for py in root.rglob("*.py"):
        src = py.read_text()
        changed = False

        def repl(m):
            nonlocal changed
            changed = True
            return m.group("field").replace("default_factory=list,\n", "")

        new = REQUIRED_LIST.sub(repl, src)

        if changed:
            py.write_text(new)
            count += 1

    return count
