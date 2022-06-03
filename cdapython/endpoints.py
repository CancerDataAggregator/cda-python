from typing import Any, Callable

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query


def _subject_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.subject_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _subject_files_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.subject_files_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _research_subject_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.research_subject_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _research_files_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.research_subject_files_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _specimen_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.specimen_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _specimen_files_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.specimen_files_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _diagnosis_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.diagnosis_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _treatments_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.treatments_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _boolean_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.boolean_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _files_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.files(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _counts_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.global_counts(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _diagnosis_counts_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.diagnosis_counts_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _researchsubject_counts_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.research_subject_counts_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _subject_counts_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.subject_counts_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _specimen_counts_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.specimen_counts_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _treatment_counts_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
) -> Endpoint:
    return api_instance.treatment_counts_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )
