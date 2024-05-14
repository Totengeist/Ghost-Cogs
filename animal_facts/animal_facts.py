import datetime
import os
import pathlib
import random
import re
import toml

from redbot.core import commands

class AnimalFacts(commands.Cog):
    """
    Retrieve a random fact about an animal found in the San Diego area
    (including zoos and aquariums).
    """

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
                self.features_used.append(i)
            else:
                self.features_available.append(i)

    @commands.command()
    async def animalfact(self, ctx, arg = "all"):
        """Get an available animal fact."""

        # Delete the command
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()

        data = self.facts_available
        date = self._today_or_date(arg)

        if arg == "all":
            data = data + self.facts_used

        elif date:
            item = self._get_date(self.facts_used, date)
            if item:
                data = [item]
            else: data = []

        if not data:
            return

        fact = random.choice(data)
        await self._print_fact(ctx, fact)

    @commands.command()
    async def animalfeature(self, ctx, arg = "all"):
        """Get an available featured animal."""

        # Delete the command
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()

        data = self.features_available
        date = self._today_or_date(arg)
        print(date)

        if arg == "all":
            data = data + self.features_used

        elif date:
            item = self._get_date(self.features_used, date)
            print(item)
            if item:
                data = [item]
            else:
                data = []

        if not data:
            return

        feature = random.choice(data)
        await self._print_feature(ctx, feature)

    def _today_or_date(self, arg):
        date = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
        if arg == "today" or date.match(arg):
            if arg == 'today':
                return datetime.datetime.today().strftime('%Y-%m-%d')
            return arg
        return None

    def _get_date(self, data, date):
        for i in data:
            if i["date"] == date:
                return i
        return None

    async def _print_fact(self, ctx, fact):
        await(ctx.send(fact["image"]))
        await(ctx.send(f'**Animal Fact of the Day: {fact["animal"]}**'))
        await(ctx.send(fact["fact"], suppress_embeds=True))

    async def _print_feature(self, ctx, feature):
        await(ctx.send(f'## {feature["animal"]} (*{feature["latin"]}*)'))
        await(ctx.send(feature["image"]))
        await(ctx.send(feature["feature"], suppress_embeds=True))

    @commands.command()
    async def listfacts(self, ctx):
        await ctx.send(f'### Facts')
        for i in self.facts_available + self.facts_used:
            if "date" in i:
                date = i['date']
            else:
                date = "Date empty"
            await ctx.send(f'`{date}    {i["animal"]}`')
        await ctx.send(f'### Features')
        for i in self.features_available + self.features_used:
            if "date" in i:
                date = i['date']
            else:
                date = "Date empty"
            await ctx.send(f'`{date}    {i["animal"]}`')
