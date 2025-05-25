# telethon_service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
import os

# 1) اقرأ الإعدادات من المتغيّرات البيئية
API_ID          = int(os.getenv("TELETHON_API_ID", "0"))
API_HASH        = os.getenv("TELETHON_API_HASH", "")
STRING_SESSION  = os.getenv("TELETHON_STRING_SESSION", "")
TARGET_BOT      = "SaudiNumberBook_bot"   # بدون الـ @
#SaudiNumberBook_bot
#dlilcomApp_bot
if not API_ID or not API_HASH or not STRING_SESSION:
    raise RuntimeError(
        "تأكد من تعيين المتغيّرات: "
        "TELETHON_API_ID, TELETHON_API_HASH, TELETHON_STRING_SESSION"
    )

# 2) اعداد العميل باستخدام StringSession
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

app = FastAPI()

class Query(BaseModel):
    number: str

@app.on_event("startup")
async def startup_event():
    await client.connect()
    if not await client.is_user_authorized():
        # لو فعّلت التحقق بخطوتين، سيطلب منك الكود في أول تشغيل
        try:
            await client.send_code_request(os.getenv("YOUR_PHONE"))
        except SessionPasswordNeededError:
            pass

@app.post("/query")
async def query_dlil(q: Query):
    try:
        async with client.conversation(TARGET_BOT, timeout=15) as conv:
            await conv.send_message(q.number)
            resp = await conv.get_response()
            return {"reply": resp.text}
    except Exception as e:
        raise HTTPException(500, f"خطأ في المحادثة: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await client.disconnect()
