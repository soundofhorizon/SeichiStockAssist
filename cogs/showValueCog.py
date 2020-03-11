import sympy
from discord.ext import commands
import discord


class ShowValueCog(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="showValue")
    def ShowValue(self, ctx, num):

        # sympyを用いてみる。変数を定義したら後は方程式などが作れる。代入も可能。計算してくれるので使いやすいのでは？
        # 策定事項：sympyの方程式を定義する際は「expr_(変数名)」を用いる。変数には_valueを語尾につけてみる。(変更してもよい)

        SIINA_value = sympy.Symbol('SIINA_value')  # 椎名の価値をここに入れる

        # M_value = sympy.Symbol('M_value')  # Mは〔MAGNIFICATION(倍率)〕の略。今回はここに椎名の個数を入れる

        M_value = int(num)

        if M_value >= 0:  # 倍率が-になることは考慮しない
            expr_SIINA = SIINA_value + (0.1 * M_value + sympy.sin(M_value) * sympy.cos(M_value ** 2)) ** 2
            value = int(expr_SIINA.subs([(SIINA_value, 100), (M_value, 1.2)]))  # ここで数値の代入を行う。辞書型が使える。
            embed = discord.Embed(title='value_view',
                                  description=f'椎名の現在の価値は{value}です。',
                                  color=0xadff2f)
            await ctx.send(embed=embed)

    @ShowValue.error
    def ShowValue_error(self, ctx, error):
        await ctx.send(error+": \n\nエラー内容\n\n" + error.text)

# このクラスをMainクラスで呼び出すとこの関数を呼び出す
def setup(bot):
    bot.add_cog(ShowValueCog(bot))
