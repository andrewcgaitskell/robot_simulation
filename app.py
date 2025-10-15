from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

x, y = 50, 50
vx, vy = 0.6, 0.4
half_side = 2.5

def get_border_squares():
    border = []
    border_set = set()
    for i in range(0, 100, 5):
        for j in range(0, 100, 5):
            if i < 5 or i >= 95 or j < 5 or j >= 95:
                border.append({'x': i, 'y': j})
                border_set.add((i, j))
    return border, border_set

@app.route("/")
async def index():
    border, _ = get_border_squares()
    return await render_template("chart.html", border=border)

@app.websocket("/ws")
async def ws():
    global x, y, vx, vy
    _, border_set = get_border_squares()
    while True:
        prev_x, prev_y = x, y

        # Take a step
        x += vx
        y += vy

        # What 5x5 cell is the center in now, and before?
        cell_x = int(x // 5) * 5
        cell_y = int(y // 5) * 5
        prev_cell_x = int(prev_x // 5) * 5
        prev_cell_y = int(prev_y // 5) * 5

        if (cell_x, cell_y) in border_set:
            # Reverse axis if entered a new cell along that axis
            if cell_x != prev_cell_x:
                vx = -vx
                x = prev_x  # step back out
            if cell_y != prev_cell_y:
                vy = -vy
                y = prev_y  # step back out

        # Clamp to keep center inside visible area
        if x - half_side < 0:
            x = half_side
            vx = abs(vx)
        if x + half_side > 100:
            x = 100 - half_side
            vx = -abs(vx)
        if y - half_side < 0:
            y = half_side
            vy = abs(vy)
        if y + half_side > 100:
            y = 100 - half_side
            vy = -abs(vy)

        await websocket.send(json.dumps({"x": x, "y": y}))
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
