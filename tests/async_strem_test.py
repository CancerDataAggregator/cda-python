import asyncio

from pandas import DataFrame, concat

from cdapython import Q
from tests.global_settings import host, table


async def main() -> None:
    q = Q("primary_disease_type = 'Lung%' AND sex = 'male'")
    print(q.to_json())
    q = q.run(host=host, table=table, async_call=True, show_sql=True, page_size=10)

    df = DataFrame()
    async for i in q.paginator(page_size=200, output="full_df"):
        df = concat([df, i])
    print(df.head())


asyncio.run(main())
