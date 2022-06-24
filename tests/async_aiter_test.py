import asyncio

from cdapython import Q
from tests.global_settings import host

v = Q('ResearchSubject.primary_disease_type = "Lung%"').run(host=host, async_call=True)
print(v)


async def main() -> None:
    async for i in v:
        print(i)


asyncio.run(main())
