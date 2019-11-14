import random
import re
import os
from datetime import datetime, timedelta
import bs4
import discord
import requests
from discord import Embed
import traceback

client = discord.Client()

bot_token = os.environ["BOT_TOKEN"]

@client.event
async def on_ready():
    game = discord.Game(f"{client.get_guild(643397152357351424).member_count}人を監視中")
    await client.change_presence(status=discord.Status.online, activity=game)

    ch = client.get_channel( 643461625663193098 )
    embed = Embed( title='Start_up', description='Botが起動しました\n現在のバージョンは**0.0.1**です', color=0x43b581 )
    embed.set_footer( text=datetime.now() )
    await ch.send( embed=embed )

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

    d = datetime.now()  # 現在時刻の取得
    time = d.strftime("%Y/%m/%d %H:%M:%S")
    embed = Embed(
        description=f'**Changed in <#{before.channel.id}>**\n\n**before**\n{before.content}\n\n**after**\n{after.content}\n\n',
        color=0x1e90ff)  # 発言内容をdescriptionにセット
    embed.set_author(name=before.author, icon_url=before.author.avatar_url, )  # ユーザー名+ID,アバターをセット
    embed.set_footer(text=f'User ID：{before.author.id} Time：{time}',
                     icon_url=before.guild.icon_url, )  # チャンネル名,時刻,鯖のアイコンをセット
    ch = before.guild.get_channel(644181970116542485)
    await ch.send(embed=embed)


@client.event  # point付与の術
async def on_message(message):
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
                        color = [0x3efd73, 0xfb407c, 0xf3f915, 0xc60000, 0xed8f10, 0xeacf13, 0x9d9d9d, 0xebb652, 0x4259fb,
                                 0x1e90ff]
                        embed = discord.Embed(description=f'{message.author.display_name}のMCIDの報告を確認したよ！',color=random.choice(color))
                        embed.set_author(name=message.author, icon_url=message.author.avatar_url, )  # ユーザー名+ID,アバターをセット
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            description=f'{message.author} さん。\n入力されたMCIDは実在しないか、又はまだ一度も整地鯖にログインしていません。\n続けて間違った入力を行うと規定によりBANの対象になることがあります。',color=0xff0000)
                        await message.channel.send(embed=embed)
                except requests.exceptions.HTTPError:
                    await message.channel.send(f'requests.exceptions.HTTPError')
            else:
                embed = discord.Embed(description="MCIDに使用できない文字が含まれています'\n続けて間違った入力を行うと規定によりBANの対象になることがあります。",color=0xff0000)
                await message.channel.send(embed=embed)

        if message.content == '!version':
            embed = discord.Embed(description="現在のバージョンは**0.0.1**です\nNow version **0.0.1** working.", color=0x4259fb)
            await message.channel.send(embed=embed)

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
        ch = message.guild.get_channel( 643461625663193098 )
        embed = Embed( title='Error_log', description=error_message, color=0xf04747 )
        embed.set_footer( text=f'channel:{message.channel}\ntime:{datetime.now()}' )
        await ch.send( embed=embed )

client.run(bot_token)