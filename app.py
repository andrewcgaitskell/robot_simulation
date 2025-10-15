from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball physics parameters (standardized)
x, y = 50, 50  # start in the center
vx, vy = 0.6, 0.4  # adjust for desired speed
radius = 1  # radius in units (diameter=2)
min_val, max_val = 0, 100

@app.route("/")
async def index():
    return await render_template("chart.html")

@app.websocket("/ws")
async def ws():
    global x, y, vx, vy
    while True:
        x += vx
        y += vy

        # Bounce at edges so the ball (center) stays fully inside the box
        if x - radius < min_val:
            x = min_val + radius
            vx = -vx
        if x + radius > max_val:
            x = max_val - radius
            vx = -vx
        if y - radius < min_val:
            y = min_val + radius
            vy = -vy
        if y + radius > max_val:
            y = max_val - radius
            vy = -vy

        await websocket.send(json.dumps({"x": x, "y": y}))
        await asyncio.sleep(0.02)  # 50 FPS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
