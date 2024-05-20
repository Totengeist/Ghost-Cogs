from .animalfacts import AnimalFacts


async def setup(bot):
    await bot.add_cog(AnimalFacts(bot))
