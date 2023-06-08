import asyncio

from global_settings import localhost
from pandas import DataFrame, concat

from cdapython import Q

# a = Q("sex = 'male'").run(host=localhost)
# print(a)
# print(a.to_dataframe())
# df = a.get_all()

# print(df.to_dataframe())


async def main():
    df = DataFrame()
    async for i in Q("sex = 'male'").set_host(localhost).run().paginator():
        tmp_df = await i
        df = concat([df, tmp_df])
    print(df.head())


asyncio.run(main())
