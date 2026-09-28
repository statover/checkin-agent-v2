1.新版 create_react_agent 对比旧版 AgentExecutor，代码少了哪些？
旧版的AgentExecutor的需要自己来去定义提示词，再创建执行器,由执行器去自动循环调工具->本地传结果->再调用本地工具->直到不需要工具->大模型给结果
新版 create_agent不需要自己去定义提示词，把循环，工具调用执行，终止判断、ReAct提示词模板全部封装再内容，不用自己来手写while循环，不用收到工具调用解析代码，只用传模型、工具、记忆就行

2.creat_agent内部的状态图在做什么循环？
做的是ReAct循环：大模型思考要不要调用工具->要调用,执行工具->把工具的结果塞给信息->给大模型思考是不是还要调用工具如果还要就继续来调用工具直到不调用工具->大模型输出自然语言回答，结束

3.新版输入格式`{"messages": [...]}` 和旧版`{"input": "..."}`有什么不同？
新版的`{"messages": [...]}`等于就是给信息存储开了个头传入了messages后面会本地部署会自动的把完整的信息列表传给agent，包含用户、ai、工具返回的全部历史信息，输入就带上完整上下文
旧版`{"input": "..."}`一次只能传递一句话，而且要自己来委会历史而不是本地的工具自动维护

4.MemorySaver 对比旧版 ConversationBufferMemory，好在哪里？
MemorySaver保存完整的LangGraph消息对象(工具调用、工具返回全部完整存)

5.thread_id 是干嘛的？
会话编号，不同的thread_id,MemorySaver根据这个id区分保存多组独立聊天会议，比如你会话编号不同的话，讲的东西也没有关系，互不干扰

6.你手写版的 history 列表，对应新版的什么？
对应的是MemorySaver
手写的history = 我们自己维护的消息列表
新版交给MenorySaver,内部存储的checkpoint检查点里面保存的是完整的messages就是等于手写的history，不用自己append追加消息

7.@tool 装饰器在新版里变了吗？
没有变化，不管是新旧Agent,@tool的写法完全一摸一样，用来把普通的Python函数包装成大模型可以看懂的工具