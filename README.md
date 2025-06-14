实验4笔记

# 一、任务1

## 1.1 测试openAI api

建立`request.json`文件

```json
{
    "model": "gpt-4o",
    "messages": [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
}
```

使用curl命令发送请求

```bash
curl https://api.chatfire.cn/v1/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"   -d "@request.json"
```

得到如下回复

```bash
D:\Desktop\02workspace\04Credit\02Yan\02Down\09requirement\04exp4>curl https://api.chatfire.cn/v1/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"   -d "@request.json"
{
  "id": "chatcmpl-BhyELGwHlCtUppJk5YQahmQETQvZS",
  "object": "chat.completion",
  "created": 1749819329,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I assist you today?",
        "refusal": null,
        "annotations": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 10,
    "total_tokens": 29,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "audio_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": "fp_ee1d74bde0"
}

```



## 1.2 设计模型

设计prompt

```json
{
    "model": "gpt-4o",
    "messages": [
        {"role": "developer", "content": "你是一个资深系统分析师，擅长将复杂需求转化为结构化DSL。"},
        {"role": "user", "content": "请为选课管理系统生成需求模型DSL，要求包含：\n\n1. [系统名称]：明确系统标识\n2. [参与者]：学生、教师、教务管理员\n3. [功能模块]\n   - 课程管理（CRUD操作）\n   - 选课流程（时间窗控制/容量限制）\n   - 课表生成（冲突检测）\n   - 成绩管理（录入/查询）\n4. [用例描述]：采用『角色-动作-对象』格式\n5. [数据模型]：包含实体关系与核心属性\n6. [业务规则]：列出选课容量、时间限制等约束\n7. [非功能性需求]：响应时间、并发处理等\n\n使用Markdown结构化输出，保留中文方括号标记模块，技术术语中英对照。"}
    ]
}
```

发送curl请求

```bash
curl https://api.chatfire.cn/v1/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"   -d "@request.json" > response.txt
```



![image-20250613202625672](pic\image-20250613202625672.png)

粘贴转换到md，得到需求模型

````markdown
# 选课管理系统需求模型DSL

## [系统名称]
- 选课管理系统（Course Enrollment Management System）

## [参与者]
- 学生（Student）
- 教师（Teacher）
- 教务管理员（Academic Administrator）

## [功能模块]

### 课程管理（Course Management）
- 创建课程（Create Course）
- 查询课程（Read Course）
- 更新课程（Update Course）
- 删除课程（Delete Course）

### 选课流程（Enrollment Process）
- 选课时间窗控制（Time Window Control for Enrollment）
- 选课容量限制（Capacity Limitation for Enrollment）

### 课表生成（Schedule Generation）
- 冲突检测（Conflict Detection）

### 成绩管理（Grade Management）
- 成绩录入（Grade Entry）
- 成绩查询（Grade Query）

## [用例描述]

- 学生-选择-课程
- 教师-更新-课程信息
- 教务管理员-创建-课程
- 学生-查询-个人课表
- 教务管理员-生成-课程表
- 教师-录入-成绩
- 学生-查询-成绩

## [数据模型]

### 实体关系（Entity-Relationship）

- `学生(Student)`:
  - 属性：学号（Student ID）、姓名（Name）、年级（Grade）
  
- `课程(Course)`:
  - 属性：课程编号（Course ID）、课程名称（Course Name）、学分（Credits）、容量（Capacity）
  
- `教师(Teacher)`:
  - 属性：教师编号（Teacher ID）、姓名（Name）、职称（Title）

- `选课记录(Enrollment Record)`:
  - 属性：记录编号（Record ID）、学生学号（Student ID）、课程编号（Course ID）

### 实体关系图（ERD）

```plaintext
学生(Student) 1..* --- 1..* 选课记录(Enrollment Record)
课程(Course) 1..* --- 1..* 选课记录(Enrollment Record)
教师(Teacher) 1..* --- 1..* 课程(Course)
```

## [业务规则]

- 每门课程的选课人数不得超过课程容量（Capacity）。
- 学生只能在选课开放时间窗口内选择课程。
- 生成课表时必须检测课程时间是否冲突。

## [非功能性需求]

- 响应时间（Response Time）：系统在正常操作条件下，应在2秒内完成用户请求的响应。
- 并发处理（Concurrent Processing）：系统需支持至少同时500名用户的并发操作而无性能下降。
````





# 二、任务2

## 2.1 测试openAI SDK



```python
from openai import OpenAI
from openai.types.chat import ChatCompletion
BASE_URL: str = "https://api.chatfire.cn/v1"
API_KEY: str = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"
client: OpenAI = OpenAI(base_url=BASE_URL, api_key=API_KEY)
completion: ChatCompletion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        ],
)

print(completion.choices[0].message)
```



![image-20250613204158540](pic\image-20250613204158540.png)

```bash
E:\01Software\04develop\02complie\anaconda3\python.exe D:\Desktop\02workspace\04Credit\02Yan\02Down\09requirement\04exp4\pythonProject1\hello.py 
ChatCompletionMessage(content='Hello! How can I assist you today?', role='assistant', function_call=None, tool_calls=None, refusal=None, annotations=[])

进程已结束，退出代码为 0

```





## 2.2 设计模型



设计prompt，随后发送

```python
from openai import OpenAI
from openai.types.chat import ChatCompletion
BASE_URL: str = "https://api.chatfire.cn/v1"
API_KEY: str = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"
client: OpenAI = OpenAI(base_url=BASE_URL, api_key=API_KEY)
completion: ChatCompletion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "你是一个资深系统分析师，擅长将复杂需求转化为结构化DSL。"},
        {"role": "user",
         "content": "请为选课管理系统生成需求模型DSL，要求包含：\n\n1. [系统名称]：明确系统标识\n2. [参与者]：学生、教师、教务管理员\n3. [功能模块]\n   - 课程管理（CRUD操作）\n   - 选课流程（时间窗控制/容量限制）\n   - 课表生成（冲突检测）\n   - 成绩管理（录入/查询）\n4. [用例描述]：采用『角色-动作-对象』格式\n5. [数据模型]：包含实体关系与核心属性\n6. [业务规则]：列出选课容量、时间限制等约束\n7. [非功能性需求]：响应时间、并发处理等\n\n使用Markdown结构化输出，保留中文方括号标记模块，技术术语中英对照。"}
    ]
)
print(completion.choices[0].message)
```

![image-20250613205250474](pic\image-20250613205250474.png)

粘贴转换到md，得到需求模型

````markdown
# [系统名称]：选课管理系统

## [参与者]
- 学生（Student）
- 教师（Teacher）
- 教务管理员（Academic Administrator）

## [功能模块]

### 课程管理（Course Management）
- CRUD操作（Create, Retrieve, Update, Delete）

### 选课流程（Course Enrollment Process）
- 时间窗控制（Time Window Control）
- 容量限制（Capacity Limit）

### 课表生成（Timetable Generation）
- 冲突检测（Conflict Detection）

### 成绩管理（Grade Management）
- 录入（Entry）
- 查询（Query）

## [用例描述]

- 学生-选择-课程
- 学生-查询-课表
- 教师-录入-成绩
- 教务管理员-管理-课程
- 教务管理员-检测-课表冲突

## [数据模型]

### 实体关系（Entity Relationship）
- **学生（Student）**
  - 学号（Student ID）
  - 姓名（Name）
  - 专业（Major）
- **教师（Teacher）**
  - 工号（Teacher ID）
  - 姓名（Name）
  - 所授课程（Course Taught）
- **课程（Course）**
  - 课程编号（Course ID）
  - 课程名称（Course Name）
  - 学分（Credits）
  - 容量（Capacity）
- **选课记录（Enrollment Record）**
  - 学号（Student ID）
  - 课程编号（Course ID）
  - 时间戳（Timestamp）
- **成绩记录（Grade Record）**
  - 学号（Student ID）
  - 课程编号（Course ID）
  - 成绩（Grade）

### 核心属性（Core Attributes）
- 时间窗的开始与结束时间（Start and End Time of Time Window）
- 课表冲突标识（Conflict Flag）

## [业务规则]

- 每门课程的选课容量限制，最多50人。
- 选课时间窗限制为学期开始后两周内。
- 学生不得选择时间冲突的课程。
- 成绩录入须在学期结束后两周内完成。

## [非功能性需求]

- 响应时间：系统操作须在2秒内完成。
- 并发处理：支持至少1000名用户同时在线操作。
- 可用性：系统需保证一年内运营时间不少于99.5%。
```

上述模型提供了一个结构化的DSL描述，用于指导选课管理系统的设计和开发。通过明确参与者、功能模块、用例、数据模型、业务规则以及非功能性需求，可以使开发人员准确理解系统的复杂需求并进行有效的实现。

````

# 三、任务3

## 3.1 环境配置

（在任务2中已经建立conda环境）

clone github项目

```bash
git clone https://github.com/openai/openai-agents-python.git
```

然后安装依赖

```bash
pip install -e .
```



## 3.2 测试Agent

编写测试对应代码

```python

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
```



![image-20250613212943869](pic\image-20250613212943869.png)



红色报错，是因为API Key用的不是官网的，即便设置了也会报错，显示「不存在这个API KEY」

```python
# 设置openai的api key
import os
os.environ["OPENAI_API_KEY"] = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"
```



## 3.3 测试工作流



编写代码如下

* 第一次回答一定需要改进
* 第三次一定接收（避免无限循环）

```python
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
```



执行结果如下

![image-20250614171226827](pic\image-20250614171226827.png)

![image-20250614174104561](pic\image-20250614174104561.png)



> 完整输出，见 `输出\3.3输出.md`





## 3.4 需求模型生成

### 3.4.1 设计

最终的设计如下：

```mermaid
graph TD
A[用户需求] --> B(需求分析代理)
B --> C(用例图代理)
C --> D(顺序图代理)
D --> E(类图代理)
E --> F(约束规则代理)
F --> G[完整设计文档]
```

设计的AI代理

| 代理           | 角色       | 输入         | 输出                    |
| -------------- | ---------- | ------------ | ----------------------- |
| `需求分析师`   | 系统分析师 | 用户需求文本 | 核心功能列表            |
| `用例设计师`   | 架构师     | 需求分析结果 | 系统用例图（角色+功能） |
| `顺序图设计师` | 交互设计师 | 用例图       | 操作步骤流程图          |
| `类设计师`     | 对象设计师 | 用例+顺序图  | 类结构（属性+方法）     |
| `OCL专家`      | 规则工程师 | 类图         | 约束条件和规则          |

**共同特点**：

- 全部使用GPT-4o模型
- 强制输出纯JSON格式（不能写解释文字）
- 前一个代理的输出是后一个代理的输入

### 3.4.2 json解析增强

并且编写了json解析增强，防止AI输出不规范内容导致程序崩溃

```python
def extract_json_from_text(text: str):
    # 尝试多种方法从文本中提取有效JSON：
    # 1. 直接解析
    # 2. 正则表达式匹配{}结构
    # 3. 自动修复常见错误：
    #    - 去除多余的逗号
    #    - 给未引用的键添加引号
    # 4. 实在不行返回原始文本
```

### 3.4.3 数据模型（DSL）设计

约定了设计文档的标准化结构，定义了如下「python类」

- `UseCaseDiagram`：用例图（包含角色和功能）
- `SequenceDiagram`：顺序图（操作步骤序列）
- `ClassDiagram`：类图（类结构+关系）
- `OCLDiagram`：约束规则（前置/后置条件）

### 3.4.4 代码流程

伪代码如下

```python
async def domain_modeling_workflow(requirements: str):
    # 1. 需求分析 → 2. 用例图 → 3. 顺序图 → 4. 类图 → 5. OCL约束
    # 每个步骤：await Runner.run(代理, 输入)
```

### 3.4.5 代码

```python
import json
import asyncio
import re
from agents import Agent, Runner, RunConfig
from agents.models.openai_provider import OpenAIProvider
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

# 增强的JSON解析函数
def extract_json_from_text(text: str):
    """从文本中提取第一个完整JSON对象"""
    # 尝试直接解析纯JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 使用正则表达式提取可能的JSON结构
    matches = re.findall(r'\{[\s\S]*?\}', text)
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass

    # 尝试修复常见的JSON格式问题
    try:
        # 处理多余的逗号
        text = re.sub(r',\s*([}\]])', r'\1', text)
        # 处理未引用的键
        text = re.sub(r'([{,])\s*(\w+)\s*:', r'\1"\2":', text)
        return json.loads(text)
    except Exception:
        # 无法解析时返回原始文本
        return {"raw_output": text}

# 定义agent
requirements_agent = Agent(
    name="requirements_analyst",
    model="gpt-4o",
    instructions=(
        "你是一个专业的系统分析师，负责分析用户输入的选课管理系统需求，"
        "识别核心业务场景和功能模块。输出必须是纯JSON格式，包含以下字段："
        "system_name: 系统名称\n"
        "core_functionalities: 核心功能列表\n"
        "primary_actors: 主要参与者列表\n"
        "business_rules: 关键业务规则描述\n"
        "重要提示：只输出JSON，不要包含任何额外解释或文本！"
    )
)

usecase_agent = Agent(
    name="usecase_designer",
    model="gpt-4o",
    instructions=(
        "根据需求分析师提供的信息，设计选课管理系统的用例图。"
        "确保包含所有主要参与者和用例，处理包含(include)和扩展(extend)关系。"
        "输出必须是纯JSON格式，结构如下："
        "{\"actors\": [\"学生\", \"教师\"], "
        "\"usecases\": [{\"name\": \"选课\", \"description\": \"...\", \"actor\": \"学生\", ...}]}"
        "重要提示：只输出JSON，不要包含任何额外解释或文本！"
    )
)

sequence_agent = Agent(
    name="sequence_designer",
    model="gpt-4o",
    instructions=(
        "基于用例图Agent提供的用例信息，为每个主要用例设计系统顺序图(SSD)。"
        "描述参与者与系统之间的交互序列，包括消息名称和参数。"
        "输出必须是纯JSON格式，结构如下："
        "{\"for_usecase\": \"选课\", "
        "\"messages\": [{\"sender\": \"学生\", \"receiver\": \"系统\", ...}]}"
        "重要提示：只输出JSON，不要包含任何额外解释或文本！"
    )
)

class_agent = Agent(
    name="class_designer",
    model="gpt-4o",
    instructions=(
        "根据系统顺序图和业务需求，识别系统中的主要概念类及其关系。"
        "包括：类名、属性、方法以及类之间的关联、聚合、组合和继承关系。"
        "输出必须是纯JSON格式，结构如下："
        "{\"classes\": [{\"name\": \"学生\", \"attributes\": [...]}], "
        "\"relationships\": [...]}"
        "重要提示：只输出JSON，不要包含任何额外解释或文本！"
    )
)

ocl_agent = Agent(
    name="ocl_specialist",
    model="gpt-4o",
    instructions=(
        "基于概念类图，为关键类和方法设计Object Constraint Language(OCL)合约。"
        "包括前置条件、后置条件和类不变式约束。"
        "输出必须是纯JSON格式，结构如下："
        "{\"constraints\": [{\"context\": \"学生\", \"type\": \"invariant\", ...}]}"
        "重要提示：只输出JSON，不要包含任何额外解释或文本！"
    )
)

'''
DSL定义
'''

# 基础模型
class DomainModel(BaseModel):
    system_name: str

# 用例图DSL
class UseCase(BaseModel):
    name: str
    description: str
    actor: str
    includes: List[str] = []
    extends: List[Dict[str, str]] = []  # {"extension_point": "", "usecase": ""}

class UseCaseDiagram(DomainModel):
    actors: List[str]
    usecases: List[UseCase]

# 系统顺序图DSL
class Message(BaseModel):
    sender: str
    receiver: str
    message: str
    parameters: Dict[str, str] = {}

class SequenceDiagram(DomainModel):
    for_usecase: str
    messages: List[Message]

# 概念类图DSL
class Attribute(BaseModel):
    name: str
    type: str
    visibility: str = "private"

class Method(BaseModel):
    name: str
    parameters: Dict[str, str] = {}
    return_type: str = "void"

class ClassRelationship(BaseModel):
    type: Literal["association", "aggregation", "composition", "inheritance"]
    from_class: str
    to_class: str
    multiplicity: str = "1"
    role: Optional[str] = None

class ClassModel(BaseModel):
    name: str
    attributes: List[Attribute] = []
    methods: List[Method] = []

class ClassDiagram(DomainModel):
    classes: List[ClassModel]
    relationships: List[ClassRelationship] = []

# OCL合约DSL
class OCLConstraint(BaseModel):
    context: str  # 类名
    type: Literal["precondition", "postcondition", "invariant"]
    name: str
    expression: str
    description: str

class OCLDiagram(DomainModel):
    constraints: List[OCLConstraint]

# 完整模型
class CompleteDomainModel(BaseModel):
    system_name: str
    usecase_diagram: UseCaseDiagram
    sequence_diagrams: List[SequenceDiagram]
    class_diagram: ClassDiagram
    ocl_diagram: OCLDiagram

# 初始化模型提供者
provider = OpenAIProvider(
    openai_client=AsyncOpenAI(base_url="https://api.chatfire.cn/v1",
                              api_key='sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON'),
    use_responses=False,
)

# 增强的工作流执行器
async def domain_modeling_workflow(requirements: str):
    # 1. 需求分析
    req_result = await Runner.run(
        requirements_agent,
        [{"content": requirements, "role": "user"}],
        run_config=RunConfig(model_provider=provider)
    )
    req_output = req_result.final_output
    print("需求分析完成")
    print(req_output)

    # 2. 用例图设计
    usecase_input = [
        {"content": req_output, "role": "user"},
        {"content": "请生成选课管理系统的用例图", "role": "user"}
    ]
    usecase_result = await Runner.run(usecase_agent, usecase_input, run_config=RunConfig(model_provider=provider))
    usecase_output = usecase_result.final_output
    print("\n用例图设计完成")
    print(usecase_output)

    # 3. 系统顺序图设计
    sequence_diagrams = []
    # 直接从文本中提取用例名称
    usecase_names = []
    if "usecases" in usecase_output:
        # 尝试解析JSON格式
        try:
            usecase_data = json.loads(usecase_output.replace('```json', '').replace('```', '').strip())
            usecase_names = [uc["name"] for uc in usecase_data["usecases"]]
        except:
            # 从文本中提取用例名称
            matches = re.findall(r'"name": "([^"]+)"', usecase_output)
            if matches:
                usecase_names = matches
            else:
                # 备用方案：尝试通过正则匹配用例名称
                name_matches = re.findall(r'["\']?name["\']?\s*:\s*["\']([^"\']+)["\']', usecase_output)
                if name_matches:
                    usecase_names = name_matches

    # 如果没有获取到用例名称，使用默认值
    if not usecase_names:
        usecase_names = ["选课", "退选", "查看课程"]
        print("使用默认用例名称列表")

    # 只处理前3个用例以避免耗时过长
    for uc_name in usecase_names[:3]:
        sequence_input = [
            {"content": usecase_output, "role": "user"},
            {"content": f"请生成用例'{uc_name}'的系统顺序图", "role": "user"}
        ]
        sequence_result = await Runner.run(sequence_agent, sequence_input,
                                           run_config=RunConfig(model_provider=provider))
        sequence_output = sequence_result.final_output
        sequence_diagrams.append(sequence_output)
        print(f"\n顺序图'{uc_name}'设计完成")
        print(sequence_output)

    # 4. 概念类图设计
    class_input = [
        {"content": usecase_output, "role": "user"},
        {"content": "\n".join(sequence_diagrams), "role": "user"},
        {"content": "请生成概念类图", "role": "user"}
    ]
    class_result = await Runner.run(class_agent, class_input, run_config=RunConfig(model_provider=provider))
    class_output = class_result.final_output
    print("\n概念类图设计完成")
    print(class_output)

    # 5. OCL合约设计
    ocl_input = [
        {"content": class_output, "role": "user"},
        {"content": "请生成OCL合约", "role": "user"}
    ]
    ocl_result = await Runner.run(ocl_agent, ocl_input, run_config=RunConfig(model_provider=provider))
    ocl_output = ocl_result.final_output
    print("\nOCL合约设计完成")
    print(ocl_output)

    # 6. 构建完整模型并返回
    complete_model = {
        "system_name": "选课管理系统",
        "usecase_diagram": usecase_output,
        "sequence_diagrams": sequence_diagrams,
        "class_diagram": class_output,
        "ocl_diagram": ocl_output
    }

    print("\n领域建模流程完成，返回最终模型")
    return complete_model

# 增强的示例运行
async def main():
    # 使用更具体的需求描述
    requirements = (
        "开发一个选课管理系统，包含以下功能：\n"
        "1. 学生功能：查看可选课程、选课、退选、查看已选课程、查看成绩\n"
        "2. 教师功能：管理课程（添加/修改/删除）、录入成绩、查看选课学生\n"
        "3. 管理员功能：管理用户（学生/教师/管理员）、管理系统参数、审核选课冲突\n"
        "4. 系统约束：选课时间冲突检测、课程容量限制、权限控制\n"
        "5. 非功能需求：响应时间<2秒、支持1000并发用户"
    )

    try:
        print("开始领域建模工作流...")
        domain_model = await domain_modeling_workflow(requirements)

        print("\n完整领域模型生成成功！")
        print("\n===== 用例图 =====")
        print(domain_model["usecase_diagram"])

        print("\n===== 系统顺序图 =====")
        for i, diagram in enumerate(domain_model["sequence_diagrams"]):
            print(f"\n顺序图 {i + 1}:\n{diagram}")

        print("\n===== 概念类图 =====")
        print(domain_model["class_diagram"])

        print("\n===== OCL合约 =====")
        print(domain_model["ocl_diagram"])

        # 保存到文件
        # with open("domain_model.json", "w", encoding="utf-8") as f:
        #     json.dump(domain_model, f, indent=2, ensure_ascii=False)
        # print("\n模型已保存到 domain_model.json")

        # 保存到文件
        with open("domain_model.md", "w", encoding="utf-8") as f:
            f.write("===== 用例图 =====\n")
            f.write(domain_model["usecase_diagram"] + "\n\n")

            f.write("===== 系统顺序图 =====\n")
            for i, diagram in enumerate(domain_model["sequence_diagrams"]):
                f.write(f"\n顺序图 {i + 1}:\n{diagram}\n")

            f.write("\n===== 概念类图 =====\n")
            f.write(domain_model["class_diagram"] + "\n")

            f.write("\n===== OCL合约 =====\n")
            f.write(domain_model["ocl_diagram"] + "\n")

        print("模型已保存到 domain_model.md")

    except Exception as e:
        print(f"\n模型生成失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.4.6 输出

见`输出/domain_model.md`



