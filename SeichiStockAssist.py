import random
import re
import os
from datetime import datetime
import bs4
import discord
import requests
from discord import Embed
import traceback
import redis
import sympy
import matplotlib.pyplot as plt
import numpy as np

# Redisに接続
pool = redis.ConnectionPool.from_url(
    url=os.environ['REDIS_URL'],
    db=0,
    decode_responses=True
)

rc = redis.StrictRedis(connection_pool=pool)

client = discord.Client()

bot_token = os.environ["BOT_TOKEN"]


@client.event
async def on_ready():
    game = discord.Game(f"{client.get_guild(643397152357351424).member_count}人を監視中")
    await client.change_presence(status=discord.Status.online, activity=game)

    ch = client.get_channel(643461625663193098)
    d = datetime.now()  # 現在時刻の取得
    time = d.strftime("%Y/%m/%d %H:%M:%S")
    embed = Embed(title='Start_up', description='Botが起動しました\n現在のバージョンは**0.0.1**です', color=0x43b581)
    embed.set_footer(text=time)
    await ch.send(embed=embed)


@client.event  # 入ってきたときの処理
async def on_member_join(member):
    if member.author.bot:
        role = discord.utils.get(member.guild.roles, name="bot")
        await member.add_roles(role)
        return
    role = discord.utils.get(member.guild.roles, name="新人")
    await member.add_roles(role)


@client.event  # 出た時の処理
async def on_member_remove(member):
    if member.author.bot:
        role = discord.utils.get(member.guild.roles, name="bot")
        await member.add_roles(role)
        return
    role = discord.utils.get(member.guild.roles, name="新人")
    await member.add_roles(role)


@client.event
async def on_message_delete(message):
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


@client.event
async def on_message_edit(before, after):
    # メッセージ送信者がBotだった場合は無視する
    if before.author.bot:
        return

    # URLが文中に含まれる場合は無視する(URLの詳細がembedで表示されるときにeditを発火するため)
    if "http" in before.content:
        return

    d = datetime.now()  # 現在時刻の取得
    time = d.strftime("%Y/%m/%d %H:%M:%S")
    embed = Embed(
        description=f"**Changed in <#{before.channel.id}>**\n\n**before**\n{before.content}\n\n**after**\n{after.content}\n\n",
        color=0x1e90ff)  # 発言内容をdescriptionにセット
    embed.set_author(name=before.author, icon_url=before.author.avatar_url, )  # ユーザー名+ID,アバターをセット
    embed.set_footer(text=f'User ID：{before.author.id} Time：{time}',
                     icon_url=before.guild.icon_url, )  # チャンネル名,時刻,鯖のアイコンをセット
    ch = before.guild.get_channel(644181970116542485)
    await ch.send(embed=embed)


@client.event  # point付与の術
async def on_message(message):
    if message.author.bot:
        return

    try:
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
                        channel = client.get_channel(CHANNEL_ID)
                        color = [0x3efd73, 0xfb407c, 0xf3f915, 0xc60000, 0xed8f10, 0xeacf13, 0x9d9d9d, 0xebb652,
                                 0x4259fb, 0x1e90ff]
                        embed = discord.Embed(description=f'{message.author.display_name}のMCIDの報告を確認したよ！',
                                              color=random.choice(color))
                        embed.set_author(name=message.author, icon_url=message.author.avatar_url, )  # ユーザー名+ID,アバターをセット
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            description=f'{message.author} さん。\n入力されたMCIDは実在しないか、又はまだ一度も整地鯖にログインしていません。\n'
                                        f'続けて間違った入力を行うと規定によりBANの対象になることがあります。',
                            color=0xff0000)
                        await message.channel.send(embed=embed)
                except requests.exceptions.HTTPError:
                    await message.channel.send(f'requests.exceptions.HTTPError')
            else:
                embed = discord.Embed(description="MCIDに使用できない文字が含まれています'\n続けて間違った入力を行うと規定によりBANの対象になることがあります。",
                                      color=0xff0000)
                await message.channel.send(embed=embed)

        # 椎名の現在の価値を表示するための関数を策定するの巻

        if message.content.startswith('!showValue'):
            channel = client.get_channel(643461625663193098)
            # sympyを用いてみる。変数を定義したら後は方程式などが作れる。代入も可能。計算してくれるので使いやすいのでは？
            # 策定事項：sympyの方程式を定義する際は「expr_(変数名)」を用いる。変数には_valueを語尾につけてみる。(変更してもよい)
            SIINA_value = sympy.Symbol('SIINA_value')  # 椎名の絶対的価値を定める
            # M_value = sympy.Symbol('M_value')  # Mは〔MAGNIFICATION(倍率)〕の略。今回はここに椎名の個数を入れる
            msg = f'{message.content}'.replace('!showValue ', '')
            M_value = int(msg)
            if M_value >= 0:  # 倍率が-になることは考慮しない
                expr_SIINA = SIINA_value + (0.1 * M_value + sympy.sin(M_value) * sympy.cos(M_value ** 2)) ** 2
                value = int(expr_SIINA.subs([(SIINA_value, 100), (M_value, 1.2)]))  # ここで数値の代入を行う。辞書型が使える。
                embed = discord.Embed(title='value_view',
                                      description=f'椎名の現在の価値は{value}です。',
                                      color=0xadff2f)
                await channel.send(embed=embed)

        if message.content.startswith("!graph"):
            x = np.linspace(0, 100, 1000)
            y = (1 / 3) * x
            plt.plot(x, y, color="green")
            message.channel.send(plt.show())

        # メッセージ削除
        if message.content.startswith('!del '):
            if discord.utils.get(message.author.roles, name="admin"):
                msg = f'{message.content}'.replace('!del ', '')
                p = re.compile(r'^[0-9]+$')
                if p.fullmatch(msg):
                    kazu = int(msg)
                    await message.channel.purge(limit=kazu + 1)
                    embed = Embed(discription=f'{kazu}件のメッセージが{message.author}によって削除されました')
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("そのコマンドは管理者以外は使用できません。")
    except:
        error_message = f'```{traceback.format_exc()}```'
        ch = message.guild.get_channel(643461625663193098)
        d = datetime.now()  # 現在時刻の取得
        time = d.strftime("%Y/%m/%d %H:%M:%S")
        embed = Embed(title='Error_log', description=error_message, color=0xf04747)
        embed.set_footer(text=f'channel:{message.channel}\ntime:{time}')
        await ch.send(embed=embed)


client.run(bot_token)
