import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = "6044511389:AAFI1a_s5wHzoDKcwvveGTeo5_bWt15_mKA"

# Function to shorten the URL using GPlinks API
def shorten_url(api_key, long_url):
    api_endpoint = "https://gplinks.in/api"
    params = {
        "api": api_key,
        "url": long_url
    }
    response = requests.post(api_endpoint, data=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("shortenedUrl"):
            return data["shortenedUrl"]
    return None


# Command handler for the /start command
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the URL Shortener Bot!\n\nPlease provide your Shortus API key by using the /apikey command.")


# Command handler for the /apikey command
def apikey(update: Update, context: CallbackContext):
    # Extract the API key provided by the user
    api_key = context.args[0]

    # Store the API key in the user's context for later use
    context.user_data['api_key'] = api_key

    context.bot.send_message(chat_id=update.effective_chat.id, text="Shortus API key successfully set!")


# Message handler for handling user messages
def handle_message(update: Update, context: CallbackContext):
    # Check if the user has provided an API key
    if 'api_key' not in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide your Shortus API key by using the /apikey command.")
        return

    # Extract the text message from the user
    message = update.message.text

    # Shorten the URL using the user's API key
    short_url = shorten_url(context.user_data['api_key'], message)

    # Send the shortened URL back to the user
    if short_url:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Short URL: {short_url}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to shorten URL.")


def main():
    # Create the Updater and pass the bot token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("apikey", apikey))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
