# Copyright 2024 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.
"""Module that provides convenient utilities for working with [PydanticAI](https://ai.pydantic.dev/)."""

import os
from typing import Any, cast

import logfire
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName

logfire.configure(send_to_logfire='if-token-present')


class MyModel(BaseModel):
    """A model that can answer questions about the cities amd country."""

    name: str
    country: str


model = cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o'))
print(f'Using model: {model}')

agent: Any = Agent(model=model, result_type=MyModel)


if __name__ == '__main__':
    from rich import print

    result = agent.run_sync('Which is the windy city?')
    print(result.data)
    print(result.cost())
    result = agent.run_sync('What is the capital of France?')
    print(result.data)
    print(result.cost())
    print(agent.last_run_messages)
