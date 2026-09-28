from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field
from config import API_KEY

class StudyPlan(BaseModel):
    """学习计划结构"""
    subject: str = Field(description="学习科目")
    duration_hours: float = Field(description="学习时长，单位小时")
    tasks: list[str] = Field(description="具体学习任务列表")

llm = ChatDeepSeek(model="deepseek-chat", api_key=API_KEY)

# ✅ function_calling模式，不需要提示词带json
structured_llm = llm.with_structured_output(StudyPlan, method="function_calling")

result = structured_llm.invoke("帮我规划今天下午学Python,3小时")

print("科目:", result.subject)
print("时长:", result.duration_hours)
print("任务列表:")
for task in result.tasks:
    print(f" -{task}")
