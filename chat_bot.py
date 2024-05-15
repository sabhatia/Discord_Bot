import discord
import bot_responses
from dotenv import load_dotenv
import os

async def send_message(message, user_message, is_private):
    try:
        response: str = bot_responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e) # Modify this later

'''
Bot setup and logging
'''
def run_discord_bot() -> None:
    bot_intents = discord.Intents.default()
    bot_intents.message_content = True
    bot_client: discord.Client = discord.Client(intents=bot_intents)

    @bot_client.event
    async def on_ready():
        print(f'{bot_client.user} is up and running!')

    @bot_client.event
    async def on_message(message):

        # prevent an infinite loop
        if message.author == bot_client.user:
            return

        # extract who said what
        user:str = str(message.author)
        user_message: str = str(message.content)
        channel: str = str(message.channel)

        # log it
        print(f'{user} on ({channel}): "{user_message}"')

        # respond to the message
        await send_message(message, user_message, False)

    # Run the client - now that event handling is defined
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot_client.run(TOKEN) # type: ignore
