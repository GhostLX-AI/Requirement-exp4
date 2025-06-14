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