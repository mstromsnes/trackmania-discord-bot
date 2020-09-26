import os
import discord
from pathlib import Path
from dotenv import load_dotenv
from webscrape import scrape_trackmania_io, save_screenshot
from datetime import date

totd = scrape_trackmania_io() # [track_name, track_author_name, author_time, image_url, medal_thumbnail]
save_screenshot(totd[3], totd[0])

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
CHANNEL = os.getenv('DISCORD_CHANNEL')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=SERVER)
    channel = discord.utils.get(guild.channels, name=CHANNEL)
    embed = discord.Embed(title=totd[0], description=f'by {totd[1]}')
    message = f"```Track: {totd[0]}\n\
Author: {totd[1]}\n\
Author Medal: {totd[2]}```"

    embed.set_author(name=totd[2], icon_url=totd[4])
    # embed.set_image(url=Path(f'./screenshots/{totd[0]}.jpg'))
    # embed.set_thumbnail(totd[4])
    # embed.add_field(name="Author", value=totd[1], inline=False)
    # embed.add_field(name="Track Name", value=totd[0], inline=False)
    embed.set_footer(text=date.today())
    # await channel.send(date.today())
    await channel.send(embed=embed)
    await channel.send(file=discord.File(Path(f'./screenshots/{totd[0]}.jpg')))
    await client.close()


client.run(TOKEN)
