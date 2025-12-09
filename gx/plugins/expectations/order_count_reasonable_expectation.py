import pandas as pd


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

