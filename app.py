from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball parameters
x, y = 50.0, 50.0
vx, vy = 0.6, 0.4
ball_radius = 0.25  # For rendering, not for collision
sensor_offsets = [-3, 0, 3]  # For rendering only

BORDER_MIN = 0
BORDER_MAX = 99

def get_border_squares():
    border = []
    for i in range(0, 100):
        for j in range(0, 100):
            if i == BORDER_MIN or i == BORDER_MAX or j == BORDER_MIN or j == BORDER_MAX:
                border.append({'x': i, 'y': j})
    return border

@app.route("/")
async def index():
    border = get_border_squares()
    return await render_template("chart.html", border=border)

@app.websocket("/ws")
async def ws():
    global x, y, vx, vy
    while True:
        prev_x, prev_y = x, y

        # Move ball
        x += vx
        y += vy

        bounced_x = False
        bounced_y = False

        # Collision with left/right walls (using center only)
        if x < BORDER_MIN + ball_radius or x > BORDER_MAX - ball_radius:
            bounced_x = True
            vx = -vx
            x = prev_x

        # Collision with top/bottom walls (using center only)
        if y < BORDER_MIN + ball_radius or y > BORDER_MAX - ball_radius:
            bounced_y = True
            vy = -vy
            y = prev_y

        debug = []
        if bounced_x or bounced_y:
            debug.append(f"Position: ({x:.8f},{y:.8f}) Velocity: ({vx:.8f},{vy:.8f})")

        # For rendering: always send 3 sensor xs (for 3 circles)
        sensors = [x + dx for dx in sensor_offsets]

        await websocket.send(json.dumps({
            "x": x,
            "y": y,
            "sensors": sensors,
            "debug": "\n".join(debug)
        }))
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
