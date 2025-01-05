from fastapi import FastAPI, Request, HTTPException, FileResponse
import asyncio
from typing import Optional
import edge_tts
import os
import tempfile
import logging

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
    try:
        communicate = edge_tts.Communicate(t, "zh-CN-XiaoxiaoNeural")  # 使用edge-tts生成TTS
        temp_dir = tempfile.gettempdir()
        audio_file = os.path.join(temp_dir, 'output.mp3')
        await communicate.save(audio_file)  # 保存为音频文件
        return FileResponse(audio_file, media_type="audio/mpeg")  # 返回音频文件
    except Exception as e:
        logging.error(f"Error generating TTS: {e}")  # 记录错误日志
        raise HTTPException(status_code=500, detail="Error generating TTS. Please check the server logs for more information.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
