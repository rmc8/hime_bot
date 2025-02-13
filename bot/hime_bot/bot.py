import discord

from .hime import Hime


class HimeBot(discord.Client):
    def __init__(self, intents: discord.Intents, hime: Hime):
        super().__init__(intents=intents)
        self.hime = hime

    async def hime_check(self, message: discord.Message):
        result = self.hime.is_chikuchiku(message.content)
        if not result.is_chikuchiku:
            return
        hime_message = self.hime.convert_hime_message(message.content).strip()
        await message.delete()
        formatted_msg = "{}({})\n{}".format(
            message.author.display_name,
            message.author.name,
            hime_message,
        )
        await message.channel.send(formatted_msg)

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        await self.hime_check(message)

    async def on_message_edit(self, _: discord.Message, after: discord.Message):
        await self.hime_check(after)
