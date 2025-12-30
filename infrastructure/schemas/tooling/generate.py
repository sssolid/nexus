import subprocess
from pathlib import Path
from .xsdata_fixups import fix_required_lists

BASE = Path("data/autocare/documentation")

SCHEMAS = {
    "pies": BASE / "pies/PIES_7_2_Documentation/PIES_7_2_XSDSchema_Rev4_2_27_2025.xsd",
    "aces": BASE / "aces/ACES_4_2_Documentation/ACES_4_2_XSDSchema_Rev2_11_19_2021.xsd",
}


def generate(name: str, xsd: Path):
    out = Path(f"infrastructure/schemas/{name}/schemas")

    subprocess.run(
        [
            "xsdata", "generate", str(xsd),
            "--package", f"infrastructure.schemas.{name}.schemas",
            "--output", "dataclasses",
            "--config", "data/xsdata.xml",
        ],
        check=True,
    )

    patched = fix_required_lists(out)
    print(f"{name.upper()} → patched {patched} required lists")


def main():
    for name, xsd in SCHEMAS.items():
        generate(name, xsd)


if __name__ == "__main__":
    main()
