from quart import Quart, render_template, websocket
import asyncio
import json

app = Quart(__name__)

# Ball physics parameters
x, y = 0.5, 0.5
vx, vy = 0.012, 0.009  # set initial speeds

@app.route("/")
async def index():
    return await render_template("chart.html")

@app.websocket("/ws")
async def ws():
    global x, y, vx, vy
    while True:
        x += vx
        y += vy

        # Bounce exactly at axes (0 and 1)
        if x < 0:
            x = 0
            vx = -vx
        if x > 1:
            x = 1
            vx = -vx
        if y < 0:
            y = 0
            vy = -vy
        if y > 1:
            y = 1
            vy = -vy

        await websocket.send(json.dumps({"x": x, "y": y}))
        await asyncio.sleep(0.02)  # 50 FPS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
