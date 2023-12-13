"""
This holds the class Endpoint and the factory overload
"""
from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint


from cdapython.factories import MUTATIONS_COUNT
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class Mutations(Entity):
    @property
    def count(self) -> "Q":
        """This will switch from the default class to a count object of the class

        Returns:
            Q: _description_
        """
        print("ran mutations/mutations.py count")
        return QFactory.create_entity(MUTATIONS_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        offset: int,
        limit: int,
        async_req: bool,
        include_total_count: bool,
        show_counts: bool,
    ) -> Endpoint:
        """
        This will call the mutation_query endpoint
        Args:
            api_instance (QueryApi): _description_
            query (Query): _description_
            version (str): _description_
            dry_run (bool): _description_
            table (str): _description_
            async_req (bool): _description_

        Returns:
            Endpoint: _description_
        """
        print("ran mutations/mutations.py _call_endpoint")
        return api_instance.mutation_query(
            query=self.query,
            dry_run=dry_run,
            offset=offset,
            limit=limit,
            async_req=async_req,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        """
        This returns a Mutation object
        """

        @staticmethod
        def create(q_object: "Q") -> "Mutations":
            """This will create the Mutation object that will return the same query passed to it

            Args:
                q_object (Q): _description_

            Returns:
                Mutations:
            """
            print("ran mutations/mutations.py create")
            return Mutations(q_object.query)
