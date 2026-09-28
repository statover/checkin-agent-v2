from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from config import API_KEY

llm = ChatDeepSeek(model="deepseek-v4-flash", api_key=API_KEY)

messages = [
    SystemMessage(content="你是一个简短回答助手"),
    HumanMessage(content="我叫小明"),
    AIMessage(content = "你好小明！"),
    HumanMessage(content="我叫什么名字？")
]

response = llm.invoke(messages)
print(response.content)
