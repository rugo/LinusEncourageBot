import discord
import random
import json
import logging as log
import os
import time

log.basicConfig(level=log.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")

# Bot will reply in 1 out of CHANCE times
DEFAULT_CHANCE = 10
CHANCES = {
    "RedRocket": 8,
    "TestServerBots": 1,
    "Cyber Security Challenge Germany": 100
}

if TOKEN is None:
    log.error("No DISCORD_TOKEN supplied in environment.")
    exit(1)


rants = json.load(open("data/rants.json"))

class MyClient(discord.Client):
    async def on_ready(self):
        log.info('Logged in as %s [%d]', self.user.name, self.user.id)
        activity = discord.Game(name="motivating devs & hackers", type=3)
        await self.change_presence(status=discord.Status.idle, activity=activity)

    async def on_message(self, message):
        # we do not want the bot to reply to itself or other bots
        if message.author.bot:
            return

        server_name = message.guild.name
        chance = CHANCES.get(server_name, DEFAULT_CHANCE)

        if random.randint(1, chance) == 1:
            log.info("Replying to Server: %s, Message: %s", server_name, message.content)
            async with message.channel.typing():
                time.sleep(random.randint(1, 2))
            await message.reply(random.choice(rants)["text"], mention_author=True)

client = MyClient()
client.run(TOKEN)
