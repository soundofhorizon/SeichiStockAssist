from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np


class GraphCog(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="graph")  # ctxを渡しておかないと引数をnumに入れられない。
    def showValue(self, ctx):
        x = np.linspace(0, 100, 1000)
        y = (1 / 3) * x
        plt.plot(x, y, color="green")
        ctx.channel.send(plt.show())


# このクラスをMainクラスで呼び出すとこの関数を呼び出す
def setup(bot):
    bot.add_cog(GraphCog(bot))
