from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from config import API_KEY

@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b

class LogCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self._last_model_run_id = None

    def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        if run_id == self._last_model_run_id:
            return
        self._last_model_run_id = run_id
        print(f"[模型调用前] 消息数: {len(messages[0])}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"[工具调用前] {serialized['name']}({input_str})")

    def on_tool_end(self, output, **kwargs):
        print(f"[工具调用后] 结果: {output.content}")

llm = ChatDeepSeek(model="deepseek-chat", api_key=API_KEY)

agent = create_agent(
    model=llm,
    tools=[add],
    system_prompt="你是一个助手，计算加法必须调用add工具，不要自己心算。",
)

result = agent.invoke(
    {"messages": [("user", "用add工具计算3加5等于多少？")]},
    config={"callbacks": [LogCallbackHandler()]}
)
print("最终:", result["messages"][-1].content)
