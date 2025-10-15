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
    tick = 0
    while True:
        prev_x, prev_y = x, y
        narrative = [f"=== Tick {tick} ==="]
        narrative.append(f"Prev position: ({prev_x:.2f}, {prev_y:.2f}), velocity: ({vx:.2f}, {vy:.2f})")

        # Take a step
        x += vx
        y += vy

        narrative.append(f"Next position: ({x:.2f}, {y:.2f})")

        # What 5x5 cell is the center in now, and before?
        cell_x = int(x // 5) * 5
        cell_y = int(y // 5) * 5
        prev_cell_x = int(prev_x // 5) * 5
        prev_cell_y = int(prev_y // 5) * 5

        narrative.append(f"Prev cell: ({prev_cell_x}, {prev_cell_y}), Next cell: ({cell_x}, {cell_y})")
        action_taken = []

        if (cell_x, cell_y) in border_set:
            narrative.append(f"Collision detected: ball center in border cell ({cell_x}, {cell_y})")
            # Reverse axis if entered a new cell along that axis
            if cell_x != prev_cell_x:
                vx = -vx
                x = prev_x  # step back out
                action_taken.append("reverse vx and step x back")
            if cell_y != prev_cell_y:
                vy = -vy
                y = prev_y  # step back out
                action_taken.append("reverse vy and step y back")
            if not action_taken:
                narrative.append("Warning: Entered a border cell, but no axis changed (possible edge case)")

        # Clamp to keep center inside visible area
        clamp_action = []
        if x - half_side < 0:
            x = half_side
            vx = abs(vx)
            clamp_action.append("clamp left")
        if x + half_side > 100:
            x = 100 - half_side
            vx = -abs(vx)
            clamp_action.append("clamp right")
        if y - half_side < 0:
            y = half_side
            vy = abs(vy)
            clamp_action.append("clamp top")
        if y + half_side > 100:
            y = 100 - half_side
            vy = -abs(vy)
            clamp_action.append("clamp bottom")

        if action_taken:
            narrative.append(f"Bounce actions: {', '.join(action_taken)}")
        if clamp_action:
            narrative.append(f"Clamp actions: {', '.join(clamp_action)}")

        narrative.append(f"Updated position: ({x:.2f}, {y:.2f}), velocity: ({vx:.2f}, {vy:.2f})")
        narrative_str = "\n".join(narrative)
        print(narrative_str)  # Only printed on server console

        await websocket.send(json.dumps({"x": x, "y": y}))
        await asyncio.sleep(0.02)
        tick += 1

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
