import asyncio

from cdapython import Q
from tests.global_settings import integration_host

v = Q('ResearchSubject.primary_disease_type = "Lung%"').run(host=integration_host)


async def main():
    async for i in v:
        print(i)


asyncio.run(main())
