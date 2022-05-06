from cda_client.api.query_api import QueryApi
from cda_client.model.query import Query


def _subject_query(
    api_instance: QueryApi,
    query: Query,
    version: str,
    dry_run: bool,
    table: str,
    async_req: bool,
):
    return api_instance.subject_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _research_subject_query(
    api_instance: QueryApi, query, version, dry_run, table: str, async_req
):
    return api_instance.research_subject_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _specimen_query(
    api_instance, query: QueryApi, version, dry_run, table: str, async_req
):
    return api_instance.specimen_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _diagnosis_query(
    api_instance: QueryApi, query, version, dry_run, table: str, async_req
):
    return api_instance.diagnosis_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _treatments_query(
    api_instance: QueryApi, query, version, dry_run, table: str, async_req
):
    return api_instance.treatments_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _boolean_query(api_instance: QueryApi, query, version, dry_run, table, async_req):
    return api_instance.boolean_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _files_query(api_instance: QueryApi, query, version, dry_run, table, async_req):
    return api_instance.files(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )


def _counts_query(api_instance: QueryApi, query, version, dry_run, table, async_req):
    return api_instance.global_counts(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )
