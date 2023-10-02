import asyncio

from pandas import DataFrame, concat

from cdapython import Q
from tests.global_settings import host, project


async def main() -> None:
    q = Q("primary_disease_type = 'Lung%'")
    q = q.run(host=host, async_call=True, show_sql=True)
    print(q)

    df = DataFrame()
    if isinstance(q, Paged_Result):
        async for i in q.paginator(page_size=200, output="full_df", show_bar=True):
            df = concat([df, i])
        print(len(df))


asyncio.run(main())


q = (
    Q("primary_disease_type = 'Lung%'")
    .SELECT("subject_id,sex")
    .ORDER_BY("subject_id")
    .run(host=host)
    .get_all()
    .to_dataframe()
)
print(len(q))
