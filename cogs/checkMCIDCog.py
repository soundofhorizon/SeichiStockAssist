import random
import re

import bs4
import requests
from discord import Embed
from discord.ext import commands
import discord


class CheckMCIDCog(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # point付与の術
    async def on_message(self, message):
        if message.author.bot:
            return

            # MCID_check
        if message.channel.id == 644182486368124939:
            mcid = f'{message.content}'.replace('\\', '')
            p = re.compile(r'^[a-zA-Z0-9_]+$')
            if p.fullmatch(message.content):
                mcid = str.lower(mcid)
                url = f"https://w4.minecraftserver.jp/player/{mcid}"
                try:
                    res = requests.get(url)
                    res.raise_for_status()
                    soup = bs4.BeautifulSoup(res.text, "html.parser")
                    td = soup.td
                    if f'{mcid}' in f'{td}':
                        role1 = discord.utils.get(message.guild.roles, name="新人")
                        role2 = discord.utils.get(message.guild.roles, name="MCID報告済み")
                        emoji = ['👍', '🙆']
                        await message.author.remove_roles(role1)
                        await message.author.add_roles(role2)
                        await message.add_reaction(random.choice(emoji))
                        CHANNEL_ID = 644182750215143424
                        channel = discord.Client().get_channel(CHANNEL_ID)
                        color = [0x3efd73, 0xfb407c, 0xf3f915, 0xc60000, 0xed8f10, 0xeacf13, 0x9d9d9d, 0xebb652,
                                 0x4259fb, 0x1e90ff]
                        embed = Embed(description=f'{message.author.display_name}のMCIDの報告を確認したよ！',
                                      color=random.choice(color))
                        embed.set_author(name=message.author,
                                         icon_url=message.author.avatar_url, )  # ユーザー名+ID,アバターをセット
                        await channel.send(embed=embed)
                    else:
                        embed = Embed(description=f'{message.author} さん。\n入力されたMCIDは実在しないか、又はまだ一度も整地鯖にログインしていません。\n'
                                                  f'続けて間違った入力を行うと規定によりBANの対象になることがあります。',
                                      color=0xff0000)
                        await message.channel.send(embed=embed)
                except requests.exceptions.HTTPError:
                    await message.channel.send(f'requests.exceptions.HTTPError')
            else:
                embed = Embed(description="MCIDに使用できない文字が含まれています'\n続けて間違った入力を行うと規定によりBANの対象になることがあります。",
                              color=0xff0000)
                await message.channel.send(embed=embed)


# このクラスをMainクラスで呼び出すとこの関数を呼び出す
def setup(bot):
    bot.add_cog(CheckMCIDCog(bot))
