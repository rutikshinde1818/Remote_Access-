==================================================
        MASTER TELEGRAM C2 BOT (Full Version)
==================================================

This is a fully featured Remote Control (C2) bot for Telegram. It supports both Windows and Linux (Kali) and includes advanced features like Camera and Video recording.

--- [ STEP 1: TELEGRAM SETUP (MOBILE) ] ---
1. Open the Telegram app on your phone.
2. Search for "@BotFather" and start a chat.
3. Send the command "/newbot" and follow the instructions to create your bot.
4. BotFather will give you a "HTTP API TOKEN". Copy this Token.
5. Now, search for "@userinfobot" or "@IDBot" in Telegram.
6. Start the chat to get your personal "User ID" (a long number). Copy this ID.

--- [ STEP 2: SCRIPT CONFIGURATION ] ---
1. Open the "main.py" file in any text editor.
2. Find the line: TOKEN = '...' and paste your API Token there.
3. Find the line: AUTHORIZED_ID = ... and paste your User ID there (without quotes).
4. Save the file.

--- [ STEP 3: SETUP FOR WINDOWS ] ---
1. Search for "CMD" in the Start menu, right-click it, and select "RUN AS ADMINISTRATOR". (This is required for features like Screenshot and Keylogger to work properly).
2. Install the required libraries:
   pip install pyTelegramBotAPI pynput pyautogui opencv-python
3. Run the bot:
   python main.py

--- [ STEP 4: SETUP FOR KALI LINUX ] ---
Always use "sudo" or run as root for full access:

Method A (Using APT - Recommended):
   sudo apt update
   sudo apt install python3-telebot python3-pynput python3-pyautogui python3-opencv

Method B (Using Virtual Environment):
   python3 -m venv bot_env
   source bot_env/bin/activate
   pip install pyTelegramBotAPI pynput pyautogui opencv-python

--- [ HOW TO RUN IN BACKGROUND (LINUX) ] ---
To keep the bot running even after closing the terminal:
   nohup python3 main.py > bot_log.txt 2>&1 &

--- [ FEATURES ] ---
Send "/start" to the bot in Telegram to see the menu:
- /vid [sec] : Record remote video (requires camera).
- /cam       : Take a silent photo from the camera.
- /ss        : Take a live screenshot of the computer.
- /keylog    : Download the typing history file.
- /ls [path] : Browse the computer's files.
- /get [file]: Download any file from the computer.
- /net       : Scan for connected network devices.
- Direct CMD : Type any terminal command (like 'ipconfig' or 'ls') to run it remotely.

==================================================
DISCLAIMER: 
This tool is built for Educational and Authorized Penetration Testing purposes ONLY. 
Do not use this script on any system without explicit permission from the owner. 
The creator is not responsible for any misuse or damage caused by this program.
==================================================
