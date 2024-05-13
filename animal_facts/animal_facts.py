import os
import pathlib
import toml

from redbot.core import commands

class AnimalFacts(commands.Cog):
    """Retrieve a random fact about an animal found in the San Diego area (including zoos and aquariums)."""

    def __init__(self, bot):
        self.bot = bot
        path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'facts-features.toml')
        data = toml.load(path)
        self.facts_available = []
        self.facts_used = []
        self.features_available = []
        self.features_used = []
        for i in data["fact"]:
            if "date" in i.keys():
                self.facts_used.append(i)
            else:
                self.facts_available.append(i)
        for i in data["feature"]:
            if "date" in i.keys():
                self.feature_used.append(i)
            else:
                self.feature_available.append(i)

    @commands.command()
    async def listfacts(self, ctx):
        """List all attractions."""
        # Your code will go here

        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()

        for i in (self.facts_available + self.facts_used + self.features_available + self.features_used):
            await(ctx.send(i["animal"]))
