"""This module implements the ropt-everest plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Type

from ropt.plugins.plan.base import PlanHandlerPlugin, PlanStepPlugin

from ._everest_config import EverestConfigStep
from ._results_table import EverestDefaultTableHandler
from ._workflow_job import EverestWorkflowJob

if TYPE_CHECKING:
    from ropt.plan import Plan
    from ropt.plugins.plan.base import PlanStep, ResultHandler

_STEP_OBJECTS: Final[dict[str, Type[PlanStep]]] = {
    "everest_config": EverestConfigStep,
    "workflow_job": EverestWorkflowJob,
}

_RESULT_HANDLER_OBJECTS: Final[dict[str, Type[ResultHandler]]] = {
    "everest_config": EverestDefaultTableHandler,
}


class EverestPlanHandlerPlugin(PlanHandlerPlugin):
    """The default plan plugin class.

    This class provides a number of result handlers:

    `Result Handlers`:
    : - A handler that adds metadata to results
        ([`metadata`][ropt.plugins.plan._metadata.DefaultMetadataHandler]).
    : - A handler that tracks optimal results
        ([`tracker`][ropt.plugins.plan._tracker.DefaultTrackerHandler]).
    """

    def create(self, name: str, plan: Plan, **kwargs: dict[str, Any]) -> ResultHandler:
        """Create a result  handler.

        See the [ropt.plugins.plan.base.PlanPlugin][] abstract base class.

        # noqa
        """
        _, _, name = name.lower().rpartition("/")
        obj = _RESULT_HANDLER_OBJECTS.get(name)
        if obj is not None:
            return obj(plan, **kwargs)

        msg = f"Unknown results handler object type: {name}"
        raise TypeError(msg)

    def is_supported(self, method: str) -> bool:
        """Check if a method is supported.

        See the [ropt.plugins.base.Plugin][] abstract base class.

        # noqa
        """
        return method.lower() in _RESULT_HANDLER_OBJECTS


class EverestPlanStepPlugin(PlanStepPlugin):
    """The default plan plugin class.

    This class provides a number of steps:

    `Steps`:
    : - A step that performs a single ensemble evaluation
        ([`evaluator`][ropt.plugins.plan.evaluator.DefaultEvaluatorStep]).
    : - A step that runs an optimization
        ([`optimizer`][ropt.plugins.plan.optimizer.DefaultOptimizerStep]).
    """

    def create(self, name: str, plan: Plan, **kwargs: Any) -> PlanStep:  # noqa: ANN401
        """Create a step.

        See the [ropt.plugins.plan.base.PlanPlugin][] abstract base class.

        # noqa
        """
        _, _, name = name.lower().rpartition("/")
        step_obj = _STEP_OBJECTS.get(name)
        if step_obj is not None:
            return step_obj(plan, **kwargs)

        msg = f"Unknown step type: {name}"
        raise TypeError(msg)

    def is_supported(self, method: str) -> bool:
        """Check if a method is supported.

        See the [ropt.plugins.base.Plugin][] abstract base class.

        # noqa
        """
        return method.lower() in _STEP_OBJECTS
