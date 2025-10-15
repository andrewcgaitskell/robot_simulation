from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball physics parameters
radius = 0.05
x, y = 0.5, 0.5
vx, vy = 0.012, 0.009  # set initial speeds for a fun bounce

@app.route("/")
async def index():
    return await render_template("chart.html")

@app.websocket("/ws")
async def ws():
    global x, y, vx, vy
    while True:
        # Update position
        x += vx
        y += vy

        # Bounce off vertical edges
        if x - radius < 0:
            x = radius
            vx = -vx
        if x + radius > 1:
            x = 1 - radius
            vx = -vx

        # Bounce off horizontal edges
        if y - radius < 0:
            y = radius
            vy = -vy
        if y + radius > 1:
            y = 1 - radius
            vy = -vy

        # Send latest position
        await websocket.send(json.dumps({"x": x, "y": y}))
        await asyncio.sleep(0.02)  # 50 FPS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
