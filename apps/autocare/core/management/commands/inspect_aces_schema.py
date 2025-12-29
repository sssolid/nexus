from django.core.management.base import BaseCommand
from xsdata.formats.dataclass.parsers import XmlParser
from apps.autocare.aces.schemas import Aces
import inspect
import json


class Command(BaseCommand):
    help = "Dump real xsdata ACES object tree for inspection"

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True)

    def handle(self, *args, **opts):
        parser = XmlParser()
        with open(opts["file"], "rb") as f:
            aces = parser.parse(f, Aces)

        app = aces.app[0]

        def walk(obj, depth=0):
            pad = "  " * depth
            out = {}

            for attr in dir(obj):
                if attr.startswith("_"):
                    continue
                try:
                    val = getattr(obj, attr)
                except Exception:
                    continue

                if callable(val):
                    continue

                t = type(val).__name__

                if isinstance(val, list):
                    out[attr] = f"LIST[{len(val)}] of {type(val[0]).__name__ if val else 'EMPTY'}"
                else:
                    out[attr] = t

            return out

        schema = {
            "aces_attrs": walk(aces),
            "first_app_attrs": walk(app),
        }

        self.stdout.write(json.dumps(schema, indent=2, default=str))
