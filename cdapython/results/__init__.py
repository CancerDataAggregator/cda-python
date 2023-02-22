from cdapython.results.factories import COLLECT_RESULT
from cdapython.results.factories.result_factory import ResultFactory

from .factories.collect_result import CollectResult

ResultFactory.add_factory(COLLECT_RESULT, CollectResult.Factory)
