# generate_session.py
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# ⇐ هنا نضع القيم حرفياً بدل getenv
API_ID       = 29246801
API_HASH     = "f88345084e4bd755734b80b29629e457"
YOUR_PHONE   = "+966574381727"

# ننشئ الجلسة
client = TelegramClient(StringSession(), API_ID, API_HASH)

async def main():
    # عند البداية سيطلب رقم الهاتف ثم الكود
    await client.start(phone=lambda: YOUR_PHONE)
    # يطبع لك session string
    print("✅ Your session string is:\n", client.session.save())
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
