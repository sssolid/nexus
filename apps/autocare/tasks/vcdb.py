# from __future__ import annotations
#
# from celery import shared_task, chain
# from django.core.management import call_command
#
#
# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, retry_kwargs={"max_retries": 8})
# def fetch_raw_vcdb_endpoint(self, endpoint: str, pagesize: int = 1000, since: str | None = None, asof: str | None = None):
#     """
#     Calls your existing management command to fetch raw pages.
#     Retries automatically on transient failures.
#     """
#     args = [endpoint, "--db", "vcdb", "--pagesize", str(pagesize)]
#     if since:
#         args += ["--since", since]
#     if asof:
#         args += ["--asof", asof]
#
#     call_command("ingest_autocare", *args)
#
#
# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, retry_kwargs={"max_retries": 5})
# def ingest_canonical_vcdb(self, endpoint: str | None = None, order: str = "auto_fk"):
#     """
#     Ingest canonical tables from raw payloads.
#     """
#     args = ["--db", "vcdb", "--order", order]
#     if endpoint:
#         args += ["--endpoint", endpoint]
#     call_command("ingest_vcdb_payloads", *args)
#
#
# @shared_task
# def vcdb_pipeline(endpoint: str, pagesize: int = 1000, since: str | None = None, asof: str | None = None):
#     """
#     One endpoint end-to-end: raw -> canonical.
#     """
#     return chain(
#         fetch_raw_vcdb_endpoint.s(endpoint=endpoint, pagesize=pagesize, since=since, asof=asof),
#         ingest_canonical_vcdb.s(endpoint=endpoint),
#     )()
