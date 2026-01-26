import yaml
from langchain_core.prompts import PromptTemplate
from requests import request

class LlmTools:

    @staticmethod
    def get_prompt(template_name):
        with open("D:\python_code\my_code\FastAPIProject\env\prompt.yml", 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        return prompts.get(template_name)

    @staticmethod
    def format_prompt(data, prompt_template_str):

        if not data or not prompt_template_str:
            raise ValueError('prompt_template_str cannot be empty')
        # 获取格式化模板
        prompt_template = PromptTemplate.from_template(prompt_template_str)
        # 获取变量名
        expected_vars = prompt_template.input_variables
        print(f"expected_vars: {expected_vars}")
        # 检查数据是否包含变量名
        fileter_vars = {k: v for k, v in data.items() if k in expected_vars}
        print(fileter_vars)
        # 检查是否缺少主要变量
        missing = set(expected_vars) - set(fileter_vars.keys())
        if missing:
            raise Exception("Missing variables: {}".format(missing))
        # 格式化prompt
        formatted_prompt = prompt_template.format(**fileter_vars)
        print(formatted_prompt)
        return formatted_prompt


    @staticmethod
    def query_dog_api(name):
        response = request("GET", f"https://api.jisuapi.com/pet/query?appkey=62aa245c6359922e&name={name}")

        if response.status_code == 200:
            response_data = response.json().get("result")
            rep_json = {
                "query": response_data["name"],
                "detail": response_data["message"]
            }
            return rep_json

        return {}

    @staticmethod
    def query_flower(name):
        print(f"query_flower---------Querying:{name}")
        response = request(
            method="GET",
            url=f"https://api.jisuapi.com/flower/query?appkey=62aa245c6359922e&name={name}"
        )
        print(f"query_flower-----resp:{response.json()}")
        rep_json = {}
        if response.status_code == 200 and response.json().get("status") == 0:
            response_data = response.json().get("result")
            rep_json = {
                "query": response_data["name"],
                "detail": response_data["floral_lang"]
            }

        return rep_json

    @staticmethod
    def query_car_code(code):
        response = request(
            method="GET",
            url=f"https://api.jisuapi.com/lsplateluck/query?lsplate={code}&appkey=62aa245c6359922e"
        )

        if response.status_code == 200:
            response_data = response.json().get("result")
            rep_json = {
                "query": response_data["lsplate"],
                "detail": response_data["characterdetail"],
            }
            return rep_json

        return {}



llm_tools = LlmTools()

if __name__ == '__main__':
    car_prompt = llm_tools.get_prompt('car')
    data = {
        "query": "京A88989"
    }
    llm_tools.format_prompt(data, car_prompt)


