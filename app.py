from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball parameters and initial state
x, y = 50, 50
vx, vy = 0.6, 0.4
half_side = 2.5  # Half of 5x5

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

        # Predict next position
        next_x = x + vx
        next_y = y + vy

        # Find which 5x5 cell the center would enter
        cell_x = int(next_x // 5) * 5
        cell_y = int(next_y // 5) * 5
        prev_cell_x = int(prev_x // 5) * 5
        prev_cell_y = int(prev_y // 5) * 5

        bounced = False

        # X direction collision (horizontal bounce)
        if (cell_x, prev_cell_y) in border_set and cell_x != prev_cell_x:
            vx = -vx
            bounced = True
            next_x = prev_x  # Step back if bounced

        # Y direction collision (vertical bounce)
        if (prev_cell_x, cell_y) in border_set and cell_y != prev_cell_y:
            vy = -vy
            bounced = True
            next_y = prev_y  # Step back if bounced

        # Corner (simultaneous) collision
        if (cell_x, cell_y) in border_set and (cell_x != prev_cell_x and cell_y != prev_cell_y):
            vx = -vx
            vy = -vy
            next_x = prev_x
            next_y = prev_y
            bounced = True

        # Move (step back if bounced, else take next step)
        x = next_x
        y = next_y

        # Clamp to keep center inside visible area
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
