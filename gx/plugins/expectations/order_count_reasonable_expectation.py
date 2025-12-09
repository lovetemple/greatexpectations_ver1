import pandas as pd
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import ColumnMapMetricProvider, column_condition_partial
from great_expectations.execution_engine import PandasExecutionEngine


def apply_custom_logic_to_column(series, logic_fn):
    """
    Apply custom logic (as a function) to a pandas Series.
    logic_fn: a function that takes one argument (x) and returns True/False.
    Returns a boolean Series.
    Example: apply_custom_logic_to_column(df["orders"], lambda x: int(x) >= 1 and int(x) <= 6)
    """
    def _logic(x):
        try:
            return logic_fn(x)
        except Exception:
            return False
    return series.apply(_logic)

class OrderCountReasonableMetricProvider(ColumnMapMetricProvider):
    condition_metric_name = "column_values.order_count_reasonable"

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        return column.apply(is_order_count_reasonable_value)

class ExpectColumnValuesToBeOrderCountReasonable(ColumnMapExpectation):
    metric_provider = OrderCountReasonableMetricProvider
    expectation_type = "expect_column_values_to_be_order_count_reasonable"
    success_keys = ("mostly",)
    default_kwarg_values = {"mostly": 1.0}
    library_metadata = {
        "tags": ["custom", "orders"],
        "contributors": ["user"]
    }
    examples = []
