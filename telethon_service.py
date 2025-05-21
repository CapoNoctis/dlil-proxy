from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os

# 1) اقرأ الإعدادات من المتغيّرات البيئية
API_ID       = int(os.getenv("TELETHON_API_ID", "0"))
API_HASH     = os.getenv("TELETHON_API_HASH", "")
STRING_SESSION = os.getenv("TELETHON_STRING_SESSION", "")
TARGET_BOT   = "dlilcomApp_bot"   # بدون الـ @

if not API_ID or not API_HASH:
    raise RuntimeError("احتاج TE..._API_ID و TE..._API_HASH في env")

# 2) اعداد العميل
client = TelegramClient(STRING_SESSION, API_ID, API_HASH)

app = FastAPI()

class Query(BaseModel):
    number: str

@app.on_event("startup")
async def startup_event():
    await client.connect()
    if not await client.is_user_authorized():
        # طلب رقم التحقق بخطوتين إذا مفعل
        try:
            await client.send_code_request(os.getenv("YOUR_PHONE"))
            # سيطلب منك الكود في أول تشغيل فقط
        except:
            pass

@app.post("/query")
async def query_dlil(q: Query):
    async with client.conversation(TARGET_BOT, timeout=15) as conv:
        await conv.send_message(q.number)
        resp = await conv.get_response()
        return {"reply": resp.text}

@app.on_event("shutdown")
async def shutdown_event():
    await client.disconnect()
