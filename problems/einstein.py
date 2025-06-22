import marimo

__generated_with = "0.14.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo
    return


@app.cell
def _(mo):
    mo.md(r"""![](.\public\e.jpg)""")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import itertools as it
    return (it,)


@app.cell
def _():
    # 剪枝，for里面排除错误选项，使用it.permutations
    data = {
        "houses": ["红", "绿", "白", "黄", "蓝"],
        "nationalities": ["英国人", "瑞典人", "丹麦人", "挪威人", "德国人"],
        "drinks": ["茶", "牛奶", "啤酒", "咖啡", "矿泉水"],
        "pets": ["狗", "鸟", "猫", "鱼", "马"],
        "cigarettes": ["PM", "DH", "BLENDS", "BM", "Prince"],
    }
    return (data,)


@app.cell
def _(data, it):
    def solve():
        for colors in it.permutations(data["houses"]):
            if colors.index("绿") + 1 != colors.index("白"):  # 规则4
                continue
            for n in it.permutations(data["nationalities"]):
                if n.index("英国人") != colors.index("红"):  # 规则1
                    continue
                if n.index("挪威人") != 0:  # 规则9
                    continue
                if abs(n.index("挪威人") - colors.index("蓝")) != 1:  # 规则14
                    continue
                for drinks in it.permutations(data["drinks"]):
                    if n.index("丹麦人") != drinks.index("茶"):  # 规则3
                        continue
                    if colors.index("绿") != drinks.index("咖啡"):  # 规则5
                        continue
                    if drinks[2] != "牛奶":  # 规则8
                        continue
                    for pets in it.permutations(data["pets"]):
                        if pets.index("狗") != n.index("瑞典人"):  # 规则2
                            continue
                        for cigs in it.permutations(data["cigarettes"]):
                            if cigs.index("PM") != pets.index("鸟"):  # 规则6
                                continue
                            if cigs.index("DH") != colors.index("黄"):  # 规则7
                                continue
                            if (
                                abs(cigs.index("BLENDS") - pets.index("猫")) != 1
                            ):  # 规则10
                                continue
                            if (
                                abs(cigs.index("DH") - pets.index("马")) != 1
                            ):  # 规则11
                                continue
                            if cigs.index("BM") != drinks.index("啤酒"):  # 规则12
                                continue
                            if cigs.index("Prince") != n.index("德国人"):  # 规则13
                                continue
                            if (
                                abs(cigs.index("BLENDS") - drinks.index("矿泉水"))
                                != 1
                            ):  # 规则15
                                continue
        yield (colors, n, drinks, pets, cigs)
    return (solve,)


@app.cell
def _(solve):
    solutions = list(solve())
    if len(solutions) <= 0:
        print("没有找到对应的解")
    else:
        solution = solutions[0]
        p = solution[1][solution[3].index("鱼")]
        print(f"{p}养鱼做宠物")
    return


if __name__ == "__main__":
    app.run()
