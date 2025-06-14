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