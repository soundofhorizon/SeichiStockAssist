import os
import traceback
from datetime import datetime

import discord
import redis
from discord import Embed
from discord.ext import commands

# Redisに接続
pool = redis.ConnectionPool.from_url(
    url=os.environ['REDIS_URL'],
    db=0,
    decode_responses=True
)

rc = redis.StrictRedis(connection_pool=pool)

# 環境変数のBOT_TOKENを引っ張り、暗示的に示す
bot_token = os.environ["BOT_TOKEN"]

# 読み込むコグの名前を格納しておく。追加したらここに追加
INITIAL_EXTENSIONS = [
    'cogs.checkMCIDCog',
    'cogs.delCog',
    'cogs.graphCog',
    'cogs.inoutCog',
    'cogs.logCog',
    'cogs.showValueCog'
]


class SeichiStockAssist(commands.Bot):

    # コンストラクタ
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡す
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        game = discord.Game(f"{self.get_guild(643397152357351424).member_count}人を監視中")
        await self.change_presence(status=discord.Status.online, activity=game)

        ch = self.get_channel(643461625663193098)
        d = datetime.now()  # 現在時刻の取得
        time = d.strftime("%Y/%m/%d %H:%M:%S")
        embed = Embed(title='Start_up', description='Botが起動しました\n現在のバージョンは**0.0.1**です', color=0x43b581)
        embed.set_footer(text=time)
        await ch.send(embed=embed)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embeds = discord.Embed(description=f"{ctx.author.mention}さん。このコマンドは管理者のみ使用可能です。")
            return await ctx.send(embed=embeds)
        else:
            error_type = error
            error_message = f'```{error.text}```'
            ch = self.get_channel(643461625663193098)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(title=f'Error_log: {error_type}', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:{ctx.channel}\ntime:{time}')
            await ch.send(embed=embed)
            await ctx.send("Sorry! 予期せぬエラーが発生しました。")


if __name__ == '__main__':
    bot = SeichiStockAssist(command_prefix='!')
    bot.run(bot_token)
