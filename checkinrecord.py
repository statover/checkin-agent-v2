from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field
from typing import Optional
from config import API_KEY

class CheckinRecord(BaseModel):
    """学习打卡记录"""
    date: str = Field(description="打卡日期，格式YYYY-MM-DD")
    content: str = Field(description="学习内容")
    duration_hours : str = Field(description="学习时长，单位小时")
    mood: Optional[str] = Field(description="学习时的心情，可选，如果用户没提就不填")

llm = ChatDeepSeek(model="deepseek-chat",api_key=API_KEY)

structured_llm = llm.with_structured_output(CheckinRecord,method="function_calling")

user_input = "2026-09-12.今天学Pydantic结构化输出，学了3个小时，感觉收获满满"

result = structured_llm.invoke(user_input)

print("打卡日期：", result.date)
print("学习内容：", result.content)
print("学习时长：", result.duration_hours)
print("心    情：", result.mood)