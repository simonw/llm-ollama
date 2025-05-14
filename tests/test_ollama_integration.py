import json

import pytest

from llm import get_async_model, get_model, schema_dsl


@pytest.mark.integration
@pytest.mark.asyncio
async def test_async_model_prompt():
    """Tests actual run. Needs llama3.2"""
    model = get_async_model("llama3.2:latest")
    response = model.prompt("a short poem about tea")
    response_text = await response.text()
    assert len(response_text) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_async_model_prompt_with_schema():
    """Tests actual run. Needs llama3.2"""
    model = get_async_model("llama3.2:latest")
    response = model.prompt(
        "Describe a nice dog with a surprising name",
        schema=schema_dsl("name, age int, bio"),
    )
    response_text = await response.text()
    assert len(response_text) > 0
    json_response = json.loads(response_text)
    assert "name" in json_response
    assert "bio" in json_response
    assert "age" in json_response
    assert isinstance(json_response["age"], int)


@pytest.mark.integration
def test_tools():
    """Test tool execution. Needs llama3.2"""

    def multiply(a: int, b: int):
        "Multiply two integers"
        return int(a) * int(b)

    model = get_model("llama3.2:latest")
    chain = model.chain("12345 * 4312", tools=[multiply])
    result = chain.text()
    assert "53231640" in result or "53,231,640" in result
