from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball parameters
x, y = 50.0, 50.0
vx, vy = 0.6, 0.4
ball_radius = 0.25  # For display, not for collision

# Borders (inside a 100x100 grid, solid walls at 0 and 99)
BORDER_MIN = 0
BORDER_MAX = 99

@app.route("/")
async def index():
    # This is only for template rendering, which is unchanged
    border = []
    for i in range(0, 100):
        for j in range(0, 100):
            if i == BORDER_MIN or i == BORDER_MAX or j == BORDER_MIN or j == BORDER_MAX:
                border.append({'x': i, 'y': j})
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

        # Collision with left/right walls
        if x < BORDER_MIN + ball_radius or x > BORDER_MAX - ball_radius:
            bounced_x = True
            vx = -vx
            x = prev_x  # Return to previous position for perfect reflection

        # Collision with top/bottom walls
        if y < BORDER_MIN + ball_radius or y > BORDER_MAX - ball_radius:
            bounced_y = True
            vy = -vy
            y = prev_y  # Return to previous position for perfect reflection

        debug = []
        if bounced_x or bounced_y:
            debug.append(f"Position: ({x:.8f},{y:.8f}) Velocity: ({vx:.8f},{vy:.8f})")

        await websocket.send(json.dumps({
            "x": x, "y": y,
            "debug": "\n".join(debug)
        }))
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
