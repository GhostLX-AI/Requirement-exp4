
import asyncio
from agents import Agent, Runner, function_tool
from agents import RunConfig,OpenAIProvider
from openai import AsyncOpenAI



@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
    model="gpt-4o"
)
provider: OpenAIProvider = OpenAIProvider(
    openai_client=AsyncOpenAI(base_url="https://api.chatfire.cn/v1", api_key='sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON'),
    use_responses=False,
)

async def main():
    result = await Runner.run(agent,
    input="What's the weather in Beijing?",
    run_config=RunConfig(model_provider=provider)
    )
    print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main())