from quart import Quart, render_template, websocket
import asyncio
import json
import math

app = Quart(__name__)

# Ball physics parameters
radius = 0.1
x = 0.5
y = 0.8
vy = 0.0
g = 0.01
energy_loss = 0.9

@app.route("/")
async def index():
    return await render_template("chart.html")

@app.websocket("/ws")
async def ws():
    global y, vy
    t = 0
    while True:
        # Ball physics update
        vy -= g
        y += vy
        if y - radius < 0:
            y = radius
            vy = -vy * energy_loss

        t += 1
        await websocket.send(json.dumps({"t": t, "y": y}))
        await asyncio.sleep(0.02)  # 50 FPS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
