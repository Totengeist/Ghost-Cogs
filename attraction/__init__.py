from .attraction import Attraction


async def setup(bot):
    await bot.add_cog(Attraction(bot))