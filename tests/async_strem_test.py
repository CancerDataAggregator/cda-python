import asyncio

from pandas import DataFrame, concat

from cdapython import Q
from tests.global_settings import host, localhost, table


async def main() -> None:
    q = Q("ResearchSubject.primary_disease_type = 'Lung%' AND sex = 'male'")
    print(q.to_json())
    q = q.run(host=host, table=table, async_call=True, show_sql=True, limit=10)

    df = DataFrame()
    async for i in q.paginator(to_df=True):
        df = concat([df, i])
    print(df.head())


asyncio.run(main())
