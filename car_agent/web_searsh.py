import json
from env.config import conf
import requests

def web_search(query:str,top_k:int)->list[dict]:
    url = conf.qwen_web_search_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conf.qwen_web_search_api_key}"
    }
    params = {
        "query": query,
        "engineType": "Generic",
        "contents":{
            "mainText": "true",
            "markdownText": "false",
            "summary": "false",
            "rerankScore": "true"
        }
    }
    print(f"query: {json.dumps(params,ensure_ascii=False,indent=4)}")
    response = requests.post(url=url, json=params, headers=headers).json()
    items = response.get("pageItems",[])
    result_list = []
    if items and len(items) > 0:
        for item in items[:top_k]:
            result_list.append({
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"],
                "publishedTime": item["publishedTime"],
            })
    return result_list


if __name__ == '__main__':
    result = web_search("鞍山美食",5)
    print(json.dumps(result,ensure_ascii=False,indent=4))