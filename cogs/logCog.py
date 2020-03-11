from datetime import datetime
from discord import Embed
from discord.ext import commands
import traceback  # エラー表示のためにインポート


class LogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            # メッセージ送信者がBotだった場合は無視する
            if before.author.bot:
                return

            # URLが文中に含まれる場合は無視する(URLの詳細がembedで表示されるときにeditを発火するため)
            if "http" in before.content:
                return

            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(
                description=f"**Changed in <#{before.channel.id}>**\n\n"
                            f"**before**\n{before.content}\n\n"
                            f"**after**\n{after.content}\n\n",
                color=0x1e90ff
            )
            embed.set_author(name=before.author, icon_url=before.author.avatar_url, )  # ユーザー名+ID,アバターをセット
            embed.set_footer(text=f'User ID：{before.author.id} Time：{time}',
                             icon_url=before.guild.icon_url, )  # チャンネル名,時刻,鯖のアイコンをセット
            ch = before.guild.get_channel(644181970116542485)
            await ch.send(embed=embed)
        except:
            error_message = f'```{traceback.format_exc()}```'
            ch = before.guild.get_channel(643461625663193098)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(title='Error_log', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:{before.channel}\ntime:{time}')
            await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author.bot:
                return

            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(description=f'**Deleted in <#{message.channel.id}>**\n\n{message.content}\n\n',
                          color=0xff0000)  # 発言内容をdescriptionにセット
            embed.set_author(name=message.author, icon_url=message.author.avatar_url, )  # ユーザー名+ID,アバターをセット
            embed.set_footer(text=f'User ID：{message.author.id} Time：{time}',
                             icon_url=message.guild.icon_url, )  # チャンネル名,時刻,鯖のアイコンをセット
            ch = message.guild.get_channel(644181970116542485)
            await ch.send(embed=embed)
        except:
            error_message = f'```{traceback.format_exc()}```'
            ch = message.guild.get_channel(643461625663193098)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(title='Error_log', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:{message.channel}\ntime:{time}')
            await ch.send(embed=embed)


def setup(bot):
    bot.add_cog(LogCog(bot))
