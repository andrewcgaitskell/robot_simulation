from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball physics parameters (standardized: only in [7.5, 92.5])
x, y = 50, 50  # start in the center
vx, vy = 0.6, 0.4
half_side = 2.5  # half of 5 units

# Calculate border squares (each is a 5x5 cell)
def get_border_squares():
    border = []
    border_set = set()
    for i in range(0, 100, 5):
        for j in range(0, 100, 5):
            if (
                i < 5 or i >= 95 or  # left or right border
                j < 5 or j >= 95     # top or bottom border
            ):
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
        x += vx
        y += vy

        # What 5x5 cell is the center of the ball in?
        cell_x = int(x // 5) * 5
        cell_y = int(y // 5) * 5

        bounced = False
        if (cell_x, cell_y) in border_set:
            # Reverse direction
            vx = -vx
            vy = -vy
            x += vx
            y += vy
            bounced = True

        # Keep the center in [2.5, 97.5] just in case
        if x - half_side < 0:
            x = half_side
            vx = -vx
        if x + half_side > 100:
            x = 100 - half_side
            vx = -vx
        if y - half_side < 0:
            y = half_side
            vy = -vy
        if y + half_side > 100:
            y = 100 - half_side
            vy = -vy

        await websocket.send(json.dumps({"x": x, "y": y}))
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

