import telegram 
from telethon import TelegramClient
from telethon.sessions import StringSession
import time

BOT_TOKEN = '6616344837:AAGAiy5b1Bdre5Bb2hV1nkMeuGjqxaf31Jk'
API_ID = '29996160' 
API_HASH = '55305b23a72c1e001a0fb21b7bfe0785'

bot = telegram.Bot(token=BOT_TOKEN)

session = "YOUR_STRING_SESSION"
client = TelegramClient(StringSession(session), API_ID, API_HASH)

async def start():
  await client.start()
  
async def get_entities(bot, update):
  await bot.send_message(
    chat_id=update.message.chat_id, 
    text="Please send me the ID of the source channel: "
  )
  
  src_chat_id = (await bot.get_updates())[0].message.text
  
  await bot.send_message(
    chat_id=update.message.chat_id,
    text="Please send me the ID of the destination channel: "  
  )
  
  dest_chat_id = (await bot.get_updates())[0].message.text

  return src_chat_id, dest_chat_id
  
async def copy_history(src_chat_id, dest_chat_id):
  
  offset = 0 
  limit = 100
  all_msgs = []

  while True:
    print(f"Fetching from {offset}")
    msgs = await client.get_messages(src_chat_id, limit=limit, offset=offset)
  
    if not msgs:
      break
  
    all_msgs.extend(msgs)
    offset += len(msgs)
    
  batch_size = 10

  for i in range(0, len(all_msgs), batch_size):
  
    msg_batch = all_msgs[i:i+batch_size]
  
    for msg in msg_batch:  
      await bot.copy_message(dest_chat_id, src_chat_id, msg.id)
      print(f"Forwarded message {msg.id}")
    
    time.sleep(1)
      
async def handle_message(bot, update):

  src_chat, dest_chat = await get_entities(bot, update)
  await copy_history(src_chat, dest_chat)
    
  await bot.send_message(
    chat_id=update.message.chat_id, 
    text="History copied!"
  )

def main():

  loop = asyncio.get_event_loop()
  loop.create_task(start())
  
  updater = Updater(BOT_TOKEN)
  
  updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
  
  updater.start_polling()
  updater.idle()

if __name__ == "__main__":
  main()
