from .animal_facts import AnimalFacts


async def setup(bot):
    await bot.add_cog(AnimalFacts(bot))
