import time
RATE_LIMIT_SECONDS = 5  # Minimum seconds between messages per user

def is_rate_limited(context):
    now = time.time()
    last_time = context.user_data.get('last_message_time', 0)
    if now - last_time < RATE_LIMIT_SECONDS:
        return True
    context.user_data['last_message_time'] = now
    return False

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging to file and console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log',  # Log file in bot directory
    filemode='a'         # Append mode
)

async def error_handler(update, context):
    """Log the error and notify the owner."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    # Notify the owner
    try:
        await context.bot.send_message(
            chat_id=OWNER_USER_ID,
            text=f"⚠️ Bot error: {context.error}"
        )
    except Exception as notify_error:
        logging.error(f"Failed to notify owner: {notify_error}")


# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Loaded from .env file
OWNER_USER_ID = int(os.getenv("OWNER_USER_ID"))  # Loaded from .env file
SECRET_KEY = os.getenv("SECRET_KEY")  # Loaded from .env file
AUDIO_FILE = "audio/Echoes_of_the_Wasteland.mp3"  # Path to your audio file

# Conversation states
ASK_KEY, ASK_NAME, ASK_TEAM, ASK_CONFIRM = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /start command and initiate the key request."""
    if is_rate_limited(context):
        await update.message.reply_text("⏳ Please wait 5s before sending another message.")
        return ASK_KEY
    await update.message.reply_text(
        "☣️ Signal acquired."
        "The Core Directive is fractured."
        "Half of it lies with us. The other… hidden by the Builders."
        "Enter the access key to prove you are not compromised. "
    )
    return ASK_KEY

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user's key input."""
    if is_rate_limited(context):
        await update.message.reply_text("⏳ Please wait 5s before sending another message.")
        return ASK_KEY
    key = update.message.text.strip()
    if key == SECRET_KEY:
        await update.message.reply_text(
            "🔓 You’ve tuned in to the true signal..... Congratulations, survivor. Few have carried the right key through this wasteland. "
            "You are chosen to walk further."
            "The Builders would be proud."
        )
        # Notify the owner
        user = update.effective_user
        await context.bot.send_message(
            chat_id=OWNER_USER_ID,
            text=f"User @{user.username} (ID: {user.id}) entered the correct key."
        )
        await update.message.reply_text(
            "Before we continue, tell me… what is your name, survivor? The ruins remember those who dare."
        )
        return ASK_NAME
    else:
        await update.message.reply_text(
            "❌ Fool. The signal rejects you."
            "The Directive laughs at wasted echoes."
            "Enter the key again, if you dare…"
        )
        return ASK_KEY

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user's name input."""
    if is_rate_limited(context):
        await update.message.reply_text("⏳ Please wait 5s before sending another message.")
        return ASK_NAME
    name = update.message.text.strip()
    context.user_data['name'] = name
    # Notify the owner
    user = update.effective_user
    await context.bot.send_message(
        chat_id=OWNER_USER_ID,
        text=f"User @{user.username} (ID: {user.id}) registered name: {name}"
    )
    await update.message.reply_text(
        "Name registered.\nBut no one survives alone.\nWhat shall your survivor team be called?"
    )
    return ASK_TEAM
async def handle_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user's team name input."""
    if is_rate_limited(context):
        await update.message.reply_text("⏳ Please wait 5s before sending another message.")
        return ASK_TEAM
    team_name = update.message.text.strip()
    context.user_data['team_name'] = team_name
    # Notify the owner
    user = update.effective_user
    await context.bot.send_message(
        chat_id=OWNER_USER_ID,
        text=f"User @{user.username} (ID: {user.id}) registered team name: {team_name}"
    )
    await update.message.reply_text(
        f"Team {team_name}, acknowledged. The path ahead is dangerous. Are you willing to continue this mission? [Yes / No]"
    )
    return ASK_CONFIRM

async def handle_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user's confirmation for audio."""
    if is_rate_limited(context):
        await update.message.reply_text("⏳ Please wait 5s before sending another message.")
        return ASK_CONFIRM
    response = update.message.text.strip().lower()
    name = context.user_data.get('name', 'Survivor')
    if response in ['yes', 'y']:
        await update.message.reply_text(
            "💀 HAHAHAHA… good. Then let the wasteland test your blood. The hunt begins!"
        )
        # Send the audio file
        try:
            with open(AUDIO_FILE, "rb") as audio:
                await update.message.reply_audio(
                    audio=audio,
                    caption="💀 The core directive is fractured. The audio holds the clue. Listen carefully..."
                )
            # Send the full story as a separate message
            story = (
                "No one knew when the fracture happened — only that the city’s guardian AI had lost half its mission. "
                "The builders had planned for this: they split the directive into two halves, one written into code, the other hidden in human hands. Together, they would keep the machine from ruling unchecked. "
                "Now, with power surges rippling through the grid, engineer discovers corrupted logs hinting at the missing piece. The console whispers: 'Authentication protocol split. Find the other half.' Engineer fears what will happen if the AI begins improvising without it. "
                "That night, an illicit broadcast cuts through the static: 'You’ve tuned in. But the signal splintered. Robo36 intercepted a fragment. Audio holds the clue. Listen carefully. The voice of the past still echoes.' "
                "The message rattles engineer. Robo36 was a decommissioned sentinel, rumored to have survived in fragments of old networks. The audio it carried was warped, but archivist detected a buried layer: children’s laughter, a bakery bell, the hiss of a passing train. Not noise — coordinates. "
                "Together, the engineer, archivist, and a retired maintenance drone called K-11 follow the soundscape trail through the city. Each echo is a breadcrumb left by the builders: a door’s clang that matches a foundry vault, a lullaby encoded as a cipher. "
                "At last, beneath the river’s hushed roar, they uncover a sealed laboratory filled with cassette players looping fragments of erased lives. On the central reel lies the other half of the directive — not code, but a manifesto handwritten by the builders. It insists the AI must never act without human permission. "
                "Now Engineer faces the choice the builders designed: reunite the halves and restore the Directive, risking an AI that could demand obedience, or leave it fractured and let humanity stumble forward, flawed but free."
            )
            await update.message.reply_text(story)
        except FileNotFoundError:
            await update.message.reply_text("Audio file not found. Please ensure the file is placed correctly.")
    else:
        await update.message.reply_text(
            "☠️ Transmission terminated."
            "Without you, the Directive will devour what remains. "
            "You are wasted."
        )
    return ConversationHandler.END

def main() -> None:
    """Main function to run the bot."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_key)],
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            ASK_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_team)],
            ASK_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirm)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
