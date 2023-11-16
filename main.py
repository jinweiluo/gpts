from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()


class RecommendationRequest(BaseModel):
    text: str


@app.get("/")
async def get_main():
    return {"message": "Welcome to Jett Luo GPTS!"}


@app.post("/recommend/")
async def recommend_song(req: RecommendationRequest):
    text = req.text
    print(text)
    try:
        # 定义外部API请求的数据
        payload = {
            "req": {
                "module": "music.ai.CAiPet",
                "method": "chat",
                "param": {
                    "uin": 853265363,
                    "userText": text  # 使用传入的 text 参数替代 userText
                }
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        external_api_url = "http://ut.y.qq.com/cgi-bin/musicu.fcg"
        response = requests.post(external_api_url, json=payload, headers=headers)
        print(response)
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="External API request failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=80)