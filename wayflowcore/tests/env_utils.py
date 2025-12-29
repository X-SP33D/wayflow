# Copyright © 2025 Oracle and/or its affiliates.
#
# This software is under the Apache License 2.0
# (LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0) or Universal Permissive License
# (UPL) 1.0 (LICENSE-UPL or https://oss.oracle.com/licenses/upl), at your option.

import os

SKIP_LLM_TESTS_ENV_VAR = "SKIP_LLM_TESTS"
SKIP_DATASTORE_TESTS_ENV_VAR = "SKIP_DATASTORE_TESTS"


def should_skip_llm_test() -> bool:
    return SKIP_LLM_TESTS_ENV_VAR in os.environ


def should_skip_datastore_test() -> bool:
    return SKIP_DATASTORE_TESTS_ENV_VAR in os.environ


from typing import Callable, Optional


def get_env_or_raise(
    env_var: str, error_type: type = Exception, skip_check: Optional[Callable[[], bool]] = None
) -> str:
    val = os.environ.get(env_var)
    if not val:
        # If specific skip check is provided, use it
        if skip_check and skip_check():
            return "skipped"

        # Default fallback: if no specific check, assume LLM test skipping applies
        # if the variable wasn't provided (backward compatibility / default behavior)
        if not skip_check and should_skip_llm_test():
            return "skipped"

        raise error_type(f"{env_var} is not set in the environment")
    return val
