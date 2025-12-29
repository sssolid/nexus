# from __future__ import annotations
#
# from collections import defaultdict
# from typing import Dict, List, Tuple
#
# from django.core.management.base import BaseCommand
#
# from apps.autocare.core.models import AutocareRawRecord
# from apps.autocare.ingest.plans import plan_endpoints
#
#
# class Command(BaseCommand):
#     help = "Report missing raw pages per VCDB endpoint (based on stored page_number sequence)."
#
#     def add_arguments(self, parser):
#         parser.add_argument("--db", default="vcdb")
#         parser.add_argument("--endpoint", default=None, help="Limit to one endpoint, e.g. /vcdb/Vehicle")
#         parser.add_argument("--since", default=None)
#         parser.add_argument("--asof", default=None)
#
#     def handle(self, *args, **opts):
#         endpoints = [opts["endpoint"]] if opts["endpoint"] else plan_endpoints()
#
#         qs = (
#             AutocareRawRecord.objects
#             .filter(source_db=opts["db"])
#             .filter(endpoint__in=endpoints)
#         )
#
#         if opts["since"] is not None:
#             qs = qs.filter(since_date=opts["since"])
#         if opts["asof"] is not None:
#             qs = qs.filter(as_of_date=opts["asof"])
#
#         qs = qs.exclude(page_number__isnull=True).values("endpoint", "page_number")
#
#         pages_by_endpoint: Dict[str, List[int]] = defaultdict(list)
#         for row in qs:
#             pages_by_endpoint[row["endpoint"]].append(int(row["page_number"]))
#
#         any_gaps = False
#
#         for ep in endpoints:
#             pages = sorted(set(pages_by_endpoint.get(ep, [])))
#             if not pages:
#                 self.stdout.write(f"{ep}: no pages stored")
#                 continue
#
#             expected = set(range(pages[0], pages[-1] + 1))
#             missing = sorted(expected - set(pages))
#             if missing:
#                 any_gaps = True
#                 self.stdout.write(f"{ep}: missing {len(missing)} pages -> {missing[:50]}{' ...' if len(missing) > 50 else ''}")
#             else:
#                 self.stdout.write(f"{ep}: OK ({pages[0]}..{pages[-1]})")
#
#         if any_gaps:
#             self.stdout.write("\nRun your raw ingestion with --start-page on the missing ranges, or schedule Celery retries.")
