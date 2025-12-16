from langchain_community.chat_models import ChatOpenAI  # 关键！阿里云百炼适配器
from langchain_core.prompts import PromptTemplate

api_key = "sk-c5b37ad58afd4d1aa1a0924a93a7459f"

# 创建 langchain_demo 模型
model = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key,
    temperature=0.7
)
# 读取prompt
prompt = PromptTemplate.from_template(
    "你是一个花语大师，请根据以下问题回答:{query} 用中文回答，不超过200个字"
)

print(model.invoke(prompt.format(query="狗尾巴草的花语是是什么？")))





