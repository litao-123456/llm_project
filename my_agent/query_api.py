from requests import request


def query_dog_api(name):
    response = request("GET", f" https://api.jisuapi.com/pet/query?appkey=62aa245c6359922e&name={name}")
    response = response.json().get("result")
    rep_json = {
        "query":response["name"],
        "detail":response["message"]
    }
    return rep_json

def query_flower(name):
    response = request(method="GET",url=f"https://api.jisuapi.com/flower/query?appkey=62aa245c6359922e&name={name}")
    print(response.json())
    response = response.json().get("result")
    rep_json = {
        "query":response["name"],
        "detail":response["floral_lang"]
    }
    return rep_json

def query_car_code(code):
    response = request(method="GET",url=f"https://api.jisuapi.com/lsplateluck/query?lsplate={code}&appkey=62aa245c6359922e")
    response = response.json().get("result")
    rep_json = {
        "query":response["lsplate"],
        "detail":response["characterdetail"],
    }
    return rep_json

if __name__ == '__main__':
    print(query_dog_api("德国牧羊犬"))
    print(query_flower("狗尾巴草"))
    print(query_car_code("冀A88888"))


