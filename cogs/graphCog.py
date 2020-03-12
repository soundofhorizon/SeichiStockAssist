from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np


class GraphCog(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="graph")  # ctxを渡しておかないと引数をnumに入れられない。
    async def Graph(self, ctx):
        x = np.linspace(0, 100, 1000)
        y = (1 / 3) * x
        plt.plot(x, y, color='green')
        plt.xlabel("xAxis", fontsize=20, fontname='serif')
        plt.ylabel("yAxis", fontsize=20, fontname='serif')
        plt.savefig('/tmp/graph.png')  # 一時ファイルに相当するので必ずtmpディレクトリに保存する
        with open('/tmp/graph.png', mode='rb') as f:
            await ctx.send_file(ctx.channel, f)

    @Graph.error
    async def Graph_error(self, ctx, error):
        await ctx.send(error + ": \n\nエラー内容\n\n" + error.text)


# このクラスをMainクラスで呼び出すとこの関数を呼び出す
def setup(bot):
    bot.add_cog(GraphCog(bot))
