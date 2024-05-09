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
        path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'attractions.toml')
        self.data = toml.load(path)

    @commands.command()
    async def attraction(self, ctx):
        """Retrieve a random attraction."""
        # Your code will go here
        slug, item = random.choice(list(self.data['attractions'].items()))
        embed = discord.Embed(title=item["name"], description=item["description"], url=item["website"])

        if "logo" in item.keys():
            embed.set_thumbnail(url=item['logo'])

        if "address" in item.keys():
            embed.add_field(name="Address", value=item["address"], inline=False)

        parking = self._descr_or_url(item, "parking", "parking_url")
        if parking != "":
            embed.add_field(name="Parking", value=parking, inline=False)

        hours = self._descr_or_url(item, "hours", "hours_url")
        if hours != "":
            embed.add_field(name="Hours", value=hours, inline=False)

        embed.set_footer(text="Attraction key: "+slug)
        await ctx.send(embed=embed)

    @commands.command()
    async def listattractions(self, ctx):
        """List all attractions."""
        # Your code will go here
        embed = discord.Embed(title="Attractions")
        for slug, item in self.data['attractions'].items():
            embed.add_field(name=slug, value=item['name'], inline=False)
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
