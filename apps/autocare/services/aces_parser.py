from xsdata.formats.dataclass.parsers import XmlParser
from apps.autocare.aces.schemas import Aces

def load_aces(path: str) -> Aces:
    parser = XmlParser()
    with open(path, "rb") as f:
        return parser.parse(f, Aces)
