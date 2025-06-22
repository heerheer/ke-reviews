import marimo

__generated_with = "0.14.5"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""两个库用于建立队列和排列组合""")
    return


@app.cell
def _():
    from itertools import combinations  # 用于生成所有组合
    from collections import deque  # 用于队列操作
    return combinations, deque


@app.cell
def _(mo):
    mo.md(r"""两个 [int] 用于数据展示""")
    return


@app.cell
def _():
    state = [0, 0, 0, 0, 0, 0, 0]  # 开始的时候所有猪都在一边
    names = ["a", "b", "c", "A", "B", "C"]  # 小猪和大猪的名字
    return names, state


@app.cell
def _(mo):
    mo.md(r"""给定猪的序号，然后返回组合是否安全""")
    return


@app.function
def is_pigs_safe(idxs: list[int]) -> bool:
    """
    传入一个idxs(即猪的索引)，检查这些猪是否安全
    """
    for idx in idxs:
        if idx < 3 and not idx + 3 in idxs:  # 这只小猪没和大猪在一起的情况下
            if any(x != idx + 3 and x >= 3 for x in idxs):  # 如果有其他大猪
                return False  # 就危险了
    return True


@app.cell
def _(mo):
    mo.md(r"""给定状态，返回两岸是否安全""")
    return


@app.function
def is_state_safe(state: list[int]) -> bool:
    """
    传入一个state(即两岸状态)，检查两岸是否安全
    state应该是一个结果而不是一个过程
    """
    for side in [0, 1]:
        if not is_pigs_safe(
            [i for i, x in enumerate(state[:6]) if x == side]
        ):  # 这边要去掉船的索引
            return False
    return True


@app.cell
def _(mo):
    mo.md(r"""最后就是获取有效 moves，也是利用上面的函数""")
    return


@app.cell
def _(combinations):
    def get_valid_moves(state: list[int]):
        """
        传入一个state(即两岸状态)，返回所有合法的移动
        """
        valid_pigs = [
            i for i, pig in enumerate(state[:6]) if pig == state[-1]
        ]  # 找到所有和船一边的猪
        valid_moves = [
            combo
            for r in [1, 2, 3]
            for combo in combinations(valid_pigs, r)
            if is_pigs_safe(combo)
        ]  # 生成所有的排列组合并筛选安全移动
        return valid_moves
    return (get_valid_moves,)


@app.cell
def _(mo):
    mo.md(
        r"""
    问题的解决方案

    - state 需要变成 tuple 来进入 set 作为判断是否已经处理过这个 state 了
    - queue 用于储存 state 和与这个 state 有关的 move，每次有新的 move 执行，添加进队列的是(new_state, moves + [move])
    """
    )
    return


@app.cell
def _(deque, get_valid_moves, names, state):
    def solve():
        visited = set()  # 记录访问过的状态
        queue = deque([(state, [])])  # 队列存储(状态, 移动序列)

        visited.add(tuple(state))  # 初始状态

        while queue:
            current_state, moves = queue.popleft()

            # 检查是否到达目标状态（所有小猪在右岸）
            if not 0 in current_state[:6]:
                for move in moves:
                    print(f"移动猪: {', '.join([names[i] for i in move])}")
                print(f"最终状态: {current_state}")
                return

            # 获取所有合法移动
            valid_moves = get_valid_moves(current_state)
            for move in valid_moves:
                new_state = current_state.copy()
                for idx in move:
                    new_state[idx] = 1 - new_state[idx]  # 执行移动
                new_state[-1] = 1 - new_state[-1]

                if not is_state_safe(new_state):  # 检查新状态是否安全
                    continue

                state_tuple = tuple(new_state)
                if state_tuple not in visited:  # 检查新状态是否已访问
                    visited.add(state_tuple)
                    # 记录移动序列
                    new_moves = moves + [move]
                    queue.append((new_state, new_moves))
        print("没找到方案")
    return


if __name__ == "__main__":
    app.run()
