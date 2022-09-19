"""
This holds the class Endpoint and the factory overload
"""
from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.factories import MUTATIONS_COUNT, MUTATIONS
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
        return QFactory.create_entity(MUTATIONS_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
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
        return api_instance.mutation_query(
            query=query,
            version=version,
            dry_run=dry_run,
            table=table,
            async_req=async_req,
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
            return Mutations(q_object.query)
