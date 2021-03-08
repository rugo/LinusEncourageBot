import discord
import random
import json
import logging as log
import os

TOKEN = os.getenv("DISCORD_TOKEN")
# Bot will, on average, reply to 1 out of CHANCE messages 
CHANCE = int(os.getenv("BOT_CHANCE", "1"))


if TOKEN is None:
    log.error("No DISCORD_TOKEN supplied in environment.")
    exit(1)


rants = json.load(open("data/rants.json"))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        activity = discord.Game(name="nothing", type=3)
        await self.change_presence(status=discord.Status.idle, activity=activity)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if random.randint(1, CHANCE) == 1:
            await message.reply(random.choice(rants)["text"], mention_author=True)

client = MyClient()
client.run(TOKEN)
