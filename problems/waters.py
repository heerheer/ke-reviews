import marimo

__generated_with = "0.14.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from collections import deque
    return (deque,)


@app.function
def get_valid_children(state: list[int]):
    """
    获取倒水状态的新的子状态
    state:[a,b] 形如[3,4]表示a瓶有3升水，b瓶有4升水
    """
    children = []
    a, b = state

    # a-> 倒空a
    if a != 0:
        children.append(("a->", [0, b]))
    # b-> 倒空b
    if b != 0:
        children.append(("b->", [a, 0]))
    # a<- 加满
    if a < 3:
        children.append(("a<-", [3, b]))
    # b<- 加满
    if b < 4:
        children.append(("b<-", [a, 4]))
    # a->b a倒入b
    if a != 0 and b < 4:
        transfer = min(a, 4 - b)
        children.append(("a->b", [a - transfer, b + transfer]))
    # b->a b倒入a
    if b != 0 and a < 3:
        transfer = min(b, 3 - a)
        children.append(("b->a", [a + transfer, b - transfer]))
    return children


@app.cell
def _(deque):
    init_state = [0, 0]
    queue = deque([(init_state, [])])
    visited = set()
    return queue, visited


@app.cell
def _(queue, visited):
    while queue:
        state, path = queue.popleft()
        print(f"当前状态: {state}, 路径: {' '.join(path)}")
        if sum(state) == 5:
            print(f"找到路径: {' '.join(path)}")
            break
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        for action, new_state in get_valid_children(state):
            new_path = path + [action]
            queue.append((new_state, new_path))
    return


if __name__ == "__main__":
    app.run()
