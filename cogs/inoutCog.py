from discord.ext import commands
import discord


class InoutCog(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # 入ってきたときの処理
    async def on_member_join(self, member):
        if member.author.bot:
            role = discord.utils.get(member.guild.roles, name="bot")
            await member.add_roles(role)
            return
        role = discord.utils.get(member.guild.roles, name="新人")
        await member.add_roles(role)

    @commands.Cog.listener()  # 出た時の処理
    async def on_member_remove(self, member):
        if member.author.bot:
            role = discord.utils.get(member.guild.roles, name="bot")
            await member.add_roles(role)
            return
        role = discord.utils.get(member.guild.roles, name="新人")
        await member.add_roles(role)


# このクラスをMainクラスで呼び出すとこの関数を呼び出す
def setup(bot):
    bot.add_cog(InoutCog(bot))
