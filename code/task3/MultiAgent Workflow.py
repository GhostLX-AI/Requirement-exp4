# 导入如下代码所需要的库
import asyncio
from typing import Literal
from dataclasses import dataclass
from agents import Agent, Runner, function_tool, TResponseInputItem, trace, RunResult
from agents.models.openai_provider import OpenAIProvider
from openai import AsyncOpenAI
from agents import RunConfig,OpenAIProvider

@dataclass
class EvaluationFeedback:
    score: Literal["pass", "needs_improvement", "fail"]
    feedback: str

# 定义agent
story_outline_generator: Agent = Agent(
    name="story_outline_generator",
    model="gpt-4o",
    instructions=(
    "You generate a very short story outline based on the user's input."
    "If there is any feedback provided, use it to improve the outline."
    ),
)

provider: OpenAIProvider = OpenAIProvider(
    openai_client=AsyncOpenAI(base_url="https://api.chatfire.cn/v1", api_key='sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON'),
    use_responses=False,
)

evaluator: Agent = Agent(
    name="evaluator",
    model="gpt-4o",
    instructions=(
        "You evaluate a story outline and decide if it's good enough."
        "If it's not good enough, you provide feedback on what needs to be improved."
        "Never give it a pass on the first try."
        # 至多运行3次
        "You must pass him during the third assessment."
    ),
    output_type=EvaluationFeedback,
)
# 定义和执行工作流
async def main() -> None:
    msg: str = input("What kind of story would you like to hear? ")
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]
    latest_outline: str | None = None
    with trace("LLM as a judge"):
        while True:
            story_outline_result: RunResult = await Runner.run(
                story_outline_generator,
                input_items,
                run_config=RunConfig(model_provider=provider)
            )
            input_items: list[TResponseInputItem] = story_outline_result.to_input_list()
            latest_outline = story_outline_result.final_output_as(str)

            print("Story outline generated")
            print(latest_outline)

            evaluator_result: RunResult = await Runner.run(evaluator, input_items, run_config=RunConfig(model_provider=provider))


            result: EvaluationFeedback = evaluator_result.final_output
            print(f"Evaluator score: {result.score}")

            if result.score == "pass":
                print("Story outline is good enough, exiting.")
                break

            print(result.feedback)
            print("Re-running with feedback")

            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})
    print(f"Final story outline: {latest_outline}")
if __name__ == "__main__":
    asyncio.run(main())