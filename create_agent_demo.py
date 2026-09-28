from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from config import API_KEY

# 1. 定义工具（@tool没变，稳定的）
@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和，传入a和b。"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积，传入a和b。"""
    return a * b

# 2. 大模型
llm = ChatDeepSeek(model="deepseek-chat", api_key=API_KEY)

# 3. 记忆（新版用InMemorySaver）
checkpointer = InMemorySaver()

# 4. 创建Agent（新版核心，注意参数名是 system_prompt）
agent = create_agent(
    model=llm,
    tools=[add, multiply],
    system_prompt="你是一个数学助手，会使用工具计算，回答简洁。",
    checkpointer=checkpointer,  # 加了就有记忆
    name="math_agent"  # 可选，给Agent起个名字
)

# 5. 调用（输入格式：messages列表）
config = {"configurable": {"thread_id": "test_001"}}

result = agent.invoke(
    {"messages": [("user", "3加4再乘5等于多少？")]},
    config=config
)

print("\n===== 第一轮完整对话历史 =====")
for msg in result["messages"]:
    print(f"[{msg.type}] {msg.content[:100] if msg.content else '(空)'}")
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"  → 调用工具: {tc['name']}({tc['args']})")
