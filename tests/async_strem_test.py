import asyncio

from pandas import DataFrame, concat

from cdapython import (
    Q,
    get_host_url,
    set_default_project_dataset,
    set_host_url,
    set_table_version,
)
from tests.global_settings import host, project


async def main() -> None:
    q = Q("primary_disease_type = 'Lung%' AND sex = 'male'")
    print(q.to_json())
    q = q.run(host=host, table=project, async_call=True, show_sql=True, page_size=10)

    df = DataFrame()
    async for i in q.paginator(page_size=200, output="full_df"):
        df = concat([df, i])
    print(df.head())


asyncio.run(main())
