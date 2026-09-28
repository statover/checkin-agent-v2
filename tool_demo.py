from langchain_core.tools import tool

@tool
def add(a : int, b : int) -> int:
    """计算两个整数的和，传入a和b两个参数。"""
    return a + b

@tool
def get_weather(city : str) -> str:
    """查询指定城市的天气，传入城市名称"""
    return f"{city}今天晴，25度"

print("工具名:",add.name)
print("工具描述:",add.description)
print("工具参数schema",add.args)

print(add.invoke({"a" : 3,"b": 5})) #作用：取值、调用函数、拿到返回结果
print(get_weather.invoke({"city" : "北京"}))