from redbot.core import commands
import toml
import os
import random
import pathlib

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
        await ctx.send(item["name"])
