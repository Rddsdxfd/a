import telebot
import requests
import json
import time

# Create a Telegram bot object
bot = telebot.TeleBot("5991058485:AAED6QEZwvcc4aAYhKA0xAkoqx2IzU0e1jw")

# Define the function to get the cryptocurrency prices
def get_crypto_prices():
    try:
        # Make a request to the CoinGecko API to get the prices of BTC and LTC
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,litecoin&vs_currencies=usd")
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response as JSON
            data = json.loads(response.text)
            
            # Return the prices of BTC and LTC
            return data["bitcoin"]["usd"], data["litecoin"]["usd"]
        else:
            # If the request was not successful, raise an exception
            raise Exception("Error getting cryptocurrency prices")
    except Exception as e:
        # If there was an error, print the error message and return None
        print(f"Error getting cryptocurrency prices: {e}")
        return None

# Define the function to send a message to the user
def send_message(chat_id, message):
    try:
        # Send the message to the user
        bot.send_message(chat_id, message)
    except Exception as e:
        # If there was an error, print the error message
        print(f"Error sending message: {e}")

# Define the function to edit a message
def edit_message(chat_id, message_id, message):
    try:
        # Edit the message
        bot.edit_message_text(message, chat_id, message_id)
    except Exception as e:
        # If there was an error, print the error message
        print(f"Error editing message: {e}")

# Define the function to check if the price has changed by at least 1%
def has_price_changed(old_price, new_price):
    # Calculate the percentage change in the price
    percentage_change = abs((new_price - old_price) / old_price) * 100
    
    # Return True if the percentage change is greater than or equal to 1%, otherwise return False
    return percentage_change >= 0.1

# Define the main function
def main():
    # Get the initial prices of BTC and LTC
    old_btc_price, old_ltc_price = get_crypto_prices()
    
    # Send the initial prices to the user
    message_id = send_message(601140054, f"BTC: ${old_btc_price}\nLTC: ${old_ltc_price}")
    
    # Continuously check for price changes
    while True:
        # Get the current prices of BTC and LTC
        new_btc_price, new_ltc_price = get_crypto_prices()
        
        # Check if the price of BTC has changed by at least 1%
        if has_price_changed(old_btc_price, new_btc_price):
            # Edit the message with the new BTC price
            edit_message(YOUR_CHAT_ID, message_id, f"BTC: ${new_btc_price}\nLTC: ${old_ltc_price}")
            
            # Update the old BTC price
            old_btc_price = new_btc_price
        
        # Check if the price of LTC has changed by at least 1%
        if has_price_changed(old_ltc_price, new_ltc_price):
            # Edit the message with the new LTC price
            edit_message(YOUR_CHAT_ID, message_id, f"BTC: ${old_btc_price}\nLTC: ${new_ltc_price}")
            
            # Update the old LTC price
            old_ltc_price = new_ltc_price
        
        # Sleep for 1 minute before checking for price changes again
        time.sleep(60)

# Run the main function
if __name__ == "__main__":
    main()
