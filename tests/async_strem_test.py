import asyncio

from global_settings import localhost, project
from pandas import DataFrame, concat

from cdapython import (
    Q,
    get_host_url,
    set_default_project_dataset,
    set_host_url,
    set_table_version,
)


async def main() -> None:
    q = Q("primary_disease_type = 'Lung%'")
    q = q.run(host=localhost, table=project, async_call=True, show_sql=True)
    print(q)

    df = DataFrame()
    async for i in q.paginator(page_size=200, output="full_df", show_bar=True):
        df = concat([df, i])
    print(df.head())


asyncio.run(main())
