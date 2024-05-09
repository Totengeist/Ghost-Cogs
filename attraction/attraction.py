import os
import pathlib
import random
import toml

from redbot.core import commands
import discord

class Attraction(commands.Cog):
    """Retrieve a random animal attraction in the San Diego area."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def attraction(self, ctx):
        """Retrieve a random attraction."""
        # Your code will go here
        path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'attractions.toml')
        data = toml.load(path)
        item = random.choice(data['attractions'])
        embed = discord.Embed(title=item["name"], description=item["description"], url=item["website"])

        if "address" in item.keys():
            embed.add_field(name="Address", value=item["address"], inline=False)

        parking = self._descr_or_url(item, "parking", "parking_url")
        if parking != "":
            embed.add_field(name="Parking", value=parking, inline=False)
        await ctx.send(embed=embed)

    def _descr_or_url(self, data, description, url):
        value = ""
        if description in data.keys() and url in data.keys():
            value = data[description]+ " \\[[more information]("+data[url]+")\\]"
        elif description in data.keys():
            value = data[description]
        elif url in data.keys():
            value = "\\[[view online]("+data[url]+")\\]"
        return value
