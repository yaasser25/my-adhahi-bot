import telebot
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import threading

# الألوان
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

TOKEN = '8741191472:AAGOKaXUWaDCuismeVw9eVoV2byiEyFKtFI'
CHAT_ID = '6357443831'
URL = "https://adhahi.dz/register/"

bot = telebot.TeleBot(TOKEN)

# 1. الرد على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ البوت شغال ومراقب للموقع بانتياز!")

# 2. وظيفة مراقبة الموقع
def check_adhahi():
    last_alive_msg = time.time()
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        
        # رسالة طمأنينة كل ساعة (3600 ثانية)
        if time.time() - last_alive_msg > 3600:
            try:
                bot.send_message(CHAT_ID, f"⏳ تحديث: البوت مازال يعمل ويبحث... الوقت الآن: {now}")
                last_alive_msg = time.time()
            except: pass

        print(f"[{now}] {YELLOW}Checking...{RESET}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(URL, headers=headers, timeout=20)
            content = response.text

            if "مفتوحة" in content or "available" in content.lower():
                msg = "🟢 ALERT: Slots are now AVAILABLE! Check the website NOW!"
                bot.send_message(CHAT_ID, msg)
                print(f"{GREEN}{msg}{RESET}")
                time.sleep(600)
            else:
                time.sleep(30)
        except Exception as e:
            print(f"[{now}] {RED}Error: {e}. Retrying...{RESET}")
            time.sleep(20) # يستنى شوية ويعاود إذا راحت الكونيكسيو

# 3. تشغيل المراقبة
monitor_thread = threading.Thread(target=check_adhahi)
monitor_thread.daemon = True
monitor_thread.start()

print(f"{GREEN}SUCCESS: Bot is Running!{RESET}")

# 4. إعادة التشغيل التلقائي في حالة حدوث خطأ في تليجرام
while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"{RED}Polling Error: {e}. Restarting Polling...{RESET}")
        time.sleep(10)

