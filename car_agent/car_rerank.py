from env.config import conf
import requests
import json

class CarReranker:
    def __init__(self):
        self.url = conf.dashscope_rerank_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {conf.dashscope_api_key}",
        }
        self.model = conf.rerank_model

    def reank(self, texts: list[str], top_k: int = 3, query: str = None):
        payload = {
            "documents": texts,
            "top_n": top_k,
            "model": self.model,
            "query": query,
        }
        print(f"payload: {json.dumps(payload, indent=4, ensure_ascii=False)}")
        res = requests.post(self.url, json=payload, headers=self.headers)
        print(f"results: {json.dumps(res.json(), indent=4, ensure_ascii=False)}")
        results = res.json().get("results")
        reranked = []
        # 将传入的list，获取到对应的index，取对应的index 里的值。作为精排筛选
        for index in results:
            idx = index["index"]
            reranked.append(texts[idx])
        return reranked

car_ranker = CarReranker()
if __name__ == '__main__':

    documents = ['奥迪','古驰','杨树林','小米汽车','小米手机','广汽传祺']
    result = car_ranker.reank(documents,top_k=3,query="汽车")
    print(result)
