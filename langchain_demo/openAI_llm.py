import os

import yaml
from openai import OpenAI


def query_llm(query):
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-c5b37ad58afd4d1aa1a0924a93a7459f",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 设置prompt
    file_path = "D:\python_code\my_code\FastAPIProject\env\prompt.yml"
    with open(file_path, "r", encoding='utf8') as f:
        prompt_text = yaml.load(f, yaml.FullLoader)
        prompt_text = prompt_text.get("query_car_prompt")
        prompt = prompt_text.format(query)

    print("begin-----------")
    print(f"prompt: {prompt}")

    completion = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )

    full_content = ""
    print("流式输出内容为：")
    for chunk in completion:
        if chunk.choices:
            full_content += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content)
    print(f"完整内容为：{full_content}")


if __name__ == '__main__':
    query_llm("帮我挑选一款20万预算的suv")