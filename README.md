
# Telegram Bot for Treasure Hunt

**Created by [@mrfox2003](https://github.com/mrfox2003)**

This is a Telegram bot for an online treasure hunt game.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   if facing any issues Use pip with --break-system-packages

   ⚠️ Risky (can break system Python).
   If you’re okay with that, just run:
   ```
   pip install -r requirements.txt --break-system-packages

   ```

2. Get your bot token from [BotFather](https://core.telegram.org/bots#botfather).

3. Create a `.env` file in the project root with the following content:
   ```
   BOT_TOKEN=your_bot_token_here
   OWNER_USER_ID=your_numeric_user_id_here
   SECRET_KEY=your_secret_key_here
   ```
   - Replace `your_bot_token_here` with your bot token
   - Replace `your_numeric_user_id_here` with your Telegram user ID (as an integer)
   - Replace `your_secret_key_here` with the secret key for the hunt

4. Place your audio file at `audio/Echoes_of_the_Wasteland.mp3`.

5. Run the bot:
   ```
   python bot.py
   ```

## Flow

- User starts with `/start`
- Bot asks for the secret key
- If correct, asks for name
- Then asks for confirmation to receive audio
- If yes, sends audio and a long message
- Notifies the owner on successful key entry

## Notes

- Ensure the audio file is in MP3 format.
- The long message in the code is a placeholder; replace it with your actual content.
