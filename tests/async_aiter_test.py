import asyncio

from cdapython import Q
from tests.global_settings import host, table

v = Q('ResearchSubject.primary_disease_type = "Lung%"')
print(v.to_json())
v = v.run(host=host, table=table, async_call=True)


async def main() -> None:
    async for i in v:
        print(i)


asyncio.run(main())
