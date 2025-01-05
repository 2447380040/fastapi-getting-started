from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import asyncio
from typing import Optional
import edge_tts
import os

app = FastAPI()

@app.get("/")
async def home():
    return "Hello, World!"

@app.get("/name")
async def name_route(name: Optional[str] = "Unknown"):
    return f"Hello, {name}!"

@app.post("/post-data")
async def post_data(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    return data

@app.get("/tts")
async def tts_route(t: str):
    communicate = edge_tts.Communicate(t, "zh-CN-XiaoxiaoNeural")  # 使用edge-tts生成TTS
    audio_file = "/tmp/output.mp3"
    await communicate.save(audio_file)  # 保存为音频文件
    return FileResponse(audio_file, media_type="audio/mpeg")  # 返回音频文件

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
