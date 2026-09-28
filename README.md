# 第一周 LangChain 学习项目：智能打卡 Agent

基于 LangChain 新版 `create_agent`（LangGraph）实现的智能学习打卡助手，支持自然语言添加打卡记录、查询学习记录，完整覆盖 Agent 开发核心流程：工具调用、中间件、对话记忆、结构化输出。

本项目为 Agent 开发学习第一周的练习代码，包含从基础大模型调用到完整 Agent 的逐步演进过程。

---

## 技术栈

- **Python** 3.10+
- **LangChain** 新版 `create_agent`（底层基于 LangGraph）
- **DeepSeek** 大语言模型 API
- **Pydantic** 结构化输出约束
- **python-dotenv** 环境变量管理

---

## 项目结构

​```
checkin_agent_v2/
├── checkin_agent_v2.py    # 【核心】新版 create_agent 打卡 Agent 主程序
├── create_agent_demo.py   # create_agent 基础用法演示
├── checkinrecord.py       # 打卡记录工具函数
├── config.py              # 配置文件
├── tool_demo.py           # @tool 装饰器用法演示
├── middleware_one.py      # 中间件演示1
├── middleware_two.py      # 中间件演示2
├── pydantic_xuexi.py      # Pydantic 结构化输出学习
├── lang_chat.py           # 大模型基础对话演示
├── day1_notes.md          # 第一天学习笔记
├── week1_review.md        # 第一周周复盘
├── .gitignore             # Git 忽略配置
​```



---

## 环境要求

- Python 3.10 及以上
- DeepSeek API Key（DeepSeek 开放平台申请）

---

## 安装依赖

```bash
pip install langchain langchain-deepseek python-dotenv

## 配置说明

在项目根目录（或上级目录）新建 `.env` 文件，写入你的 API Key：

```env
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥

## 核心运行方法
python checkin_agent_v2.py

## 运行后在控制台输入自然语言指令，例如：
帮我记录今天学LangChain，2小时
今天一共学了多久？

## 其他演示脚本
python create_agent_demo.py   # create_agent 工具调用+中间件演示
python tool_demo.py           # @tool 装饰器演示
python lang_chat.py           # 基础大模型对话演示

## 核心功能
### 智能打卡 Agent（checkin_agent_v2.py）

- `自然语言添加学习打卡记录（内容 + 时长）
- `自然语言查询打卡记录（今日 / 总计)
- `大模型自动识别意图，选择调用对应工具
- `工具执行结果自动回传给大模型，生成自然语言回答
- `完整的 Agent 思考 - 调用工具 - 观察结果 - 再思考循环

### 中间件（middleware_one.py/middleware_two.py）

- `on_model_start`：模型调用前钩子，打印当前消息数
- `on_model_end`：模型调用后钩子，打印最后一条消息
- `on_tool_start`：工具调用前钩子，打印工具名和参数
-  `on_tool_end`：工具调用后钩子，打印工具返回结果
-  可观察 Agent 内部完整执行流程，方便调试

### 结构化输出（pydantic_xuexi.py）

- 使用 Pydantic 定义输出格式
- `with_structured_output` 约束大模型输出固定 JSON
-  `method="function_calling"` 适配 DeepSeek 支持的约束方式
-  分类任务后处理：关键词匹配 + 兜底标签

## 第一周学习知识点

1. **LangChain 核心组件**：LLM / Message / Tool / Agent / Memory
2. **@tool 装饰器**：将普通 Python 函数包装为大模型可调用的工具，自动生成名称、描述、参数 Schema
3. **手写 function-calling 循环**：理解 Agent 底层 "思考→调工具→观察→再思考" 的循环原理
4. **新版 create_agent**：基于 LangGraph 的标准 Agent，替代旧版 AgentExecutor
5. **AgentMiddleware 中间件**：在模型调用、工具调用前后插入自定义逻辑，用于日志、调试、监控
6. **对话记忆**：`InMemorySaver` + `thread_id` 实现多轮对话状态持久化
7. **结构化输出**：Pydantic + `with_structured_output` 让大模型输出固定格式 JSON，方便程序解析
8. **RAG 基础**：文档加载（TextLoader/PyPDFLoader）、递归字符分割（RecursiveCharacterTextSplitter）、嵌入向量、余弦相似度检索