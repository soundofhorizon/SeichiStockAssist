from discord import Embed
from discord.ext import commands


class DelCog(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="del")
    @commands.has_permissions(manage_guilds=True)  # これでOK
    async def delete(self, ctx, num):
        kazu = int(num)
        await ctx.channel.purge(limit=kazu + 1)
        embed = Embed(discription=f'{kazu}件のメッセージが{ctx.author}によって削除されました')
        await ctx.channel.send(embed=embed)


# このクラスをMainクラスで呼び出すとこの関数を呼び出す
def setup(bot):
    bot.add_cog(DelCog(bot))
