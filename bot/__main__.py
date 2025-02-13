import os

import discord
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from hime_bot.hime import Hime
from hime_bot.bot import HimeBot

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(THIS_DIR, ".env"))


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    hime = Hime(llm=llm)
    hb = HimeBot(intents=intents, hime=hime)
    hb.run(os.getenv("discord_api_token"))


if __name__ == "__main__":
    main()
