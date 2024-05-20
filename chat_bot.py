import discord
import bot_responses
from dotenv import load_dotenv
import os
from weather_main import Weather
from datetime import datetime

weather_prefix: str = "@weather"
load_dotenv()
WEATHER_USER = os.getenv('METOMATICS_USERNAME')
WEATHER_PASS = os.getenv('METOMATICS_PASSWORD')    
weather_bot = Weather(WEATHER_USER, WEATHER_PASS)

async def send_message(message, user_message, is_private):

    # Check if it is a weather message
    if (user_message[:8] == weather_prefix):
        print('Matched Weather prefix')
        local_time: str = datetime.now().strftime("%Y-%m-%dT%H:%MZ")
        local_pos = '37.2752,121.6853'
        weather_req:str = weather_bot.build_request(local_time, local_pos)
        weather_rsp = weather_bot.get_weather_data(weather_req)
        temp, uv_indx, wind_dir, wind_speed = weather_bot.parse_weather_rsp(weather_rsp)
        response:str = f"Today\'s Weather\nTemp: {temp}\xb0 C\nUV-Index (0-12): {uv_indx}\nWind Speed: {wind_speed} m/s\nWind Direction: {wind_dir}\xb0"
    else:
        response: str = bot_responses.get_response(user_message)
    try:
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
