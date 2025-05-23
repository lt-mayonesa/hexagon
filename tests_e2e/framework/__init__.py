import pytest

# we want to have pytest assert introspection in the helpers
pytest.register_assert_rewrite("tests_e2e.tests.utils.assertions")
