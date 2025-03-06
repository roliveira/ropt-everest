# type: ignore
# ruff: noqa

from ropt_everest import EverestPlan
from pathlib import Path


example = "basic"


def run_plan_basic(plan):
    optimizer = plan.add_optimizer()
    tracker = plan.add_tracker(optimizer)
    plan.add_table(optimizer)
    optimizer.run()


def run_plan_two_optimizers(plan):
    optimizer = plan.add_optimizer()
    tracker = plan.add_tracker(optimizer)
    plan.add_table(optimizer)

    print("Running first optimizer...")
    optimizer.run()

    config = plan.config_copy()
    config["optimization"]["max_function_evaluations"] = 2

    print("Running second optimizer...")
    optimizer.run(config=config, variables=tracker.variables)


def run_plan_loop(plan):
    optimizer = plan.add_optimizer()
    tracker = plan.add_tracker(optimizer, what="last")
    plan.add_table(optimizer)

    config = plan.config_copy()
    config["optimization"]["max_function_evaluations"] = 2
    for idx in range(3):
        optimizer.run(
            config=config,
            variables=tracker.variables,
            metadata={"iteration": idx},
        )
        print(tracker.dataframe("results"))


def run_plan_evaluation(plan):
    evaluator = plan.add_evaluator()
    tracker = plan.add_tracker(evaluator, what="all")
    evaluator.run(variables=[[0, 0, 0], [1, 1, 1]])
    print(tracker.dataframe("results"))


def run_plan(plan):
    match example:
        case "basic":
            return run_plan_basic(plan)
        case "two_optimizers":
            return run_plan_two_optimizers(plan)
        case "loop":
            return run_plan_loop(plan)
        case "evaluation":
            return run_plan_evaluation(plan)


if __name__ == "__main__":
    import warnings

    warnings.filterwarnings("ignore")
    EverestPlan.everest(Path(__file__).with_suffix(".yml"))
