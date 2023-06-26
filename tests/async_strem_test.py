import asyncio

from invoke import Result
from pandas import DataFrame, concat

from cdapython import Q
from cdapython.results.page_result import Paged_Result
from tests.global_settings import localhost, project


async def main() -> None:
    q = Q("primary_disease_type = 'Lung%'")
    q = q.run(host=localhost, table=project, async_call=True, show_sql=True)
    print(q)

    df = DataFrame()
    if isinstance(q, Paged_Result):
        async for i in q.paginator(page_size=200, output="full_df", show_bar=True):
            df = concat([df, i])
        print(len(df))


asyncio.run(main())


# q = (
#     Q("primary_disease_type = 'Lung%'")
#     .run(host=localhost, table=project)
#     .get_all()
#     .to_dataframe()
# )
# print(len(q))
