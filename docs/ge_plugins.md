# Custom Great Expectations plugins

Place custom expectations and plugins in this directory.

## Creating Custom Expectations

To create a custom expectation, create a Python file in this directory:

```python
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation

class ExpectColumnValuesToBeCustom(ColumnMapExpectation):
    """Expect column values to meet custom criteria."""
    
    # Implementation here
    pass
```

See the [Great Expectations documentation](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/overview) for more details.
