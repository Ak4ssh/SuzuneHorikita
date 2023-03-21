import pyrogram
import requests
import random
from src import pbot as app

# Define a function to get a random truth or dare question from an API
def get_question(category):
    url = f"https://api.truthordarebot.xyz/{category}"
    response = requests.get(url)
    data = response.json()
    question = data["result"]["question"]
    return question

# Define a handler for the /truth command
@app.on_message(pyrogram.filters.command("truth"))
def truth_command_handler(client, message):
    question = get_question("truth")
    client.send_message(message.chat.id, f"Truth question: {question}")

# Define a handler for the /dare command
@app.on_message(pyrogram.filters.command("dare"))
def dare_command_handler(client, message):
    question = get_question("dare")
    client.send_message(message.chat.id, f"Dare question: {question}")
