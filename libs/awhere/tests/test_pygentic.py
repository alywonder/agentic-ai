# Copyright 2024 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.


from typing import Any

import pytest
from awhere.pygentic import agent
from pydantic_ai import Agent, models
from pydantic_ai.messages import (
    Message,
    ModelAnyResponse,
    ModelStructuredResponse,
    ToolCall,
)
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.models.test import TestModel

pytestmark = pytest.mark.anyio
models.ALLOW_MODEL_REQUESTS = False


def test_agent_windy_city_with_test_model(set_event_loop: None) -> None:
    """Test that the agent correctly identifies Chicago as the Windy City using a test model."""
    with agent.override(model=TestModel()):
        result = agent.run_sync('Which is the windy city?')
        assert result.data.name.lower() == 'a'
        assert result.data.country.lower() == 'a'


def test_agent_windy_city_with_function_model(set_event_loop: None) -> None:
    """Test that the agent correctly identifies Chicago as the Windy City using a function model."""

    def return_model(_: list[Message], info: AgentInfo) -> ModelAnyResponse:
        assert info.result_tools is not None
        args_json = '{"name": "Chicago", "country": "United States"}'
        return ModelStructuredResponse(
            calls=[ToolCall.from_json(info.result_tools[0].name, args_json)]
        )

    with agent.override(model=FunctionModel(return_model)):
        result = agent.run_sync('Which is the windy city?')
        assert result.data.name.lower() == 'chicago'
        assert result.data.country.lower() == 'united states'


def test_result_tuple(set_event_loop: None) -> None:
    """Test that the agent correctly returns a tuple."""

    def return_tuple(_: list[Message], info: AgentInfo) -> ModelAnyResponse:
        assert info.result_tools is not None
        args_json = '{"response": ["foo", "bar"]}'
        return ModelStructuredResponse(
            calls=[ToolCall.from_json(info.result_tools[0].name, args_json)]
        )

    agent: Agent[Any, tuple[str, str]] = Agent(
        FunctionModel(return_tuple), result_type=tuple[str, str]
    )

    result = agent.run_sync('Hello')
    assert result.data == ('foo', 'bar')
