from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from config import API_KEY

@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b

llm = ChatDeepSeek(model="deepseek-chat", api_key=API_KEY)

class LogMiddleware(AgentMiddleware):
    def on_model_start(self, state, *, handler):
        print(f"[模型调用前] 消息数: {len(state['messages'])}")
        return handler(state)

    def on_tool_start(self, state, tool_call, *, handler):
        print(f"[工具调用前] {tool_call['name']} 参数:{tool_call['args']}")
        return handler(state, tool_call)

agent = create_agent(
    model=llm,
    tools=[add],
    system_prompt="""你必须严格遵守规则：只要是加法计算，**绝对不能自己计算**，一定要调用add工具。
不要直接输出答案，必须调用工具拿到结果之后，再整理回答。""",
    middleware=[LogMiddleware()]
)
# 强制让模型使用工具
result = agent.invoke({"messages": [("user", "请调用add工具，参数a=3，b=5，执行加法")]})
print("最终:", result["messages"][-1].content)
