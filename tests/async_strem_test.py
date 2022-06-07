import asyncio

from pandas import DataFrame, concat

from cdapython import query, Q
from tests.global_settings import host, localhost


async def main() -> None:
    q = Q("ResearchSubject.primary_disease_type = 'Lung%' and sex = 'male'")
    print(q.to_json())
    q = q.run(host=host, async_call=True)

    df = DataFrame()
    async for i in q.paginator(to_df=True):
        print(len(i))
        df = concat([df, i])
    print(df.head())


asyncio.run(main())
