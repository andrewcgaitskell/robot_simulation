from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball sensor parameters
x, y = 50, 50
vx, vy = 0.6, 0.4
circle_radius = 0.25      # Each circle: diameter 1 units
circle_spacing = 3        # Center-to-center distance
sensor_offsets = [-circle_spacing, 0, circle_spacing]  # x-offsets for left, center, right

def get_border_squares():
    border = []
    border_set = set()
    for i in range(0, 100):
        for j in range(0, 100):
            if i == 0 or i == 99 or j == 0 or j == 99:
                border.append({'x': i, 'y': j})
                border_set.add((i, j))
    return border, border_set

@app.route("/")
async def index():
    border, _ = get_border_squares()
    return await render_template("chart.html", border=border)

# Helper: which 1x1 cell is a point in?
def cell_of(px, py):
    return (int(px), int(py))

@app.websocket("/ws")
async def ws():
    global x, y, vx, vy
    _, border_set = get_border_squares()
    while True:
        prev_x, prev_y = x, y

        # Move
        x += vx
        y += vy

        # Determine for each sensor circle if it entered a border cell
        bounced_x = False
        bounced_y = False
        debug = []

        for dx in sensor_offsets:
            cx = x + dx
            cy = y
            prev_cx = prev_x + dx
            prev_cy = prev_y
            cell = cell_of(cx, cy)
            prev_cell = cell_of(prev_cx, prev_cy)

            if cell in border_set:
                # Bounce on x if we entered a new cell in x
                if cell[0] != prev_cell[0]:
                    bounced_x = True
                    debug.append(f"Circle at ({cx:.2f},{cy:.2f}) bounced X at cell {cell}")
                # Bounce on y if we entered a new cell in y
                if cell[1] != prev_cell[1]:
                    bounced_y = True
                    debug.append(f"Circle at ({cx:.2f},{cy:.2f}) bounced Y at cell {cell}")

        if bounced_x:
            vx = -vx
            x = prev_x
        if bounced_y:
            vy = -vy
            y = prev_y
        if bounced_x or bounced_y:
            debug.insert(0, f"Position: ({x:.2f},{y:.2f}) Velocity: ({vx:.2f},{vy:.2f})")

        await websocket.send(json.dumps({
            "x": x, "y": y,
            "sensors": [x + dx for dx in sensor_offsets],
            "debug": "\n".join(debug)
        }))
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

