import json
import os
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from config import API_KEY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(BASE_DIR, "checkin.json")

def load_records():
    """读取打卡记录，一定返回列表，绝不会返回None"""
    if not os.path.exists(file_name):
        return []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data is None or not isinstance(data, list):
                return []
            return data
    except (json.JSONDecodeError, Exception):
        return []

def save_records(records):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

@tool
def add_record(content: str, hour: str) -> str:
    """新增一条学习打卡记录。
    参数：content=学习内容, hour=学习时长
    """
    records = load_records()
    records.append({"学习内容": content, "学习时间": hour})
    save_records(records)
    return f"打卡成功！已记录：{content}，时长{hour}"

@tool
def show_records() -> str:
    """查看所有打卡记录。"""
    records = load_records()
    if not records:
        return "暂无打卡记录"
    return "\n".join([f"{i+1}. {r['学习内容']} - {r['学习时间']}" for i, r in enumerate(records)])

@tool
def delete_record(index: int) -> str:
    """删除指定序号的打卡记录。参数：index=序号（从1开始）"""
    records = load_records()
    if 1 <= index <= len(records):
        removed = records.pop(index - 1)
        save_records(records)
        return f"已删除：{removed['学习内容']}"
    return "序号不存在"

@tool
def update_record(index: int, content: str, hour: str) -> str:
    """修改指定序号的打卡记录。
    参数：index=序号（从1开始）, content=新内容, hour=新时长
    """
    records = load_records()
    if 1 <= index <= len(records):
        records[index - 1] = {"学习内容": content, "学习时间": hour}
        save_records(records)
        return f"已修改第{index}条记录"
    return "序号不存在"

llm = ChatDeepSeek(model="deepseek-chat", api_key=API_KEY)
checkpointer = InMemorySaver()

agent = create_agent(
    model=llm,
    tools = [add_record, show_records, delete_record, update_record],
    system_prompt="你是一个学习打卡助手，可以帮用户记录、查看、修改、删除打卡记录。用自然语言和用户交流，操作完成后告诉用户结果。",
    checkpointer=checkpointer,
    name="checkin_agent"
)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "default_user"}}
    print("===== 智能打卡助手 v2（新版 create_agent）=====")
    print("输入 exit 退出\n")
    
    while True:
        user_input = input("你: ")
        if user_input.lower() == "exit":
            print("助手: 明天继续加油！")
            break
        
        result = agent.invoke(
            {"messages": [("user", user_input)]},
            config=config
        )
        print("助手:", result["messages"][-1].content)