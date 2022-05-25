import asyncio

from pandas import DataFrame, concat

from cdapython import query, Q
from tests.global_settings import host, localhost


async def main():
    q = query("ResearchSubject.primary_disease_type LIKE 'Lung%'").run(host=host)

    df = DataFrame()
    async for i in q.paginator(to_df=True):
        print(len(i))
        df = concat([df, i])
    print(df.head())


asyncio.run(main())
