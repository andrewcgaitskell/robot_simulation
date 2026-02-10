from quart import Quart, render_template, websocket
import asyncio
import json

import math

import geopandas as gpd
from shapely.geometry import Point

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

@app.route("/bouncing")
async def index():
    border = get_border_squares()
    return await render_template("chart.html", border=border)

def smooth_peanut_outline_pixels(
    grid_size=100, r=20, cx1=32, cx2=68, cy=50, thickness=1.5, p=4.5
):
    import math
    pixels = []
    for x in range(grid_size):
        for y in range(grid_size):
            d1 = math.hypot(x - cx1, y - cy)
            d2 = math.hypot(x - cx2, y - cy)
            blend = ((d1**p + d2**p) ** (1/p))
            if abs(blend - r) < thickness:
                pixels.append({"x": x, "y": y})
    return pixels

def peanut_outline_pixels(
    grid_size=100, radius=22, cx1=38, cy1=50, cx2=62, cy2=50
):
    """
    Returns a list of {"x": int, "y": int} dicts representing the outline
    of the union of two circles (a peanut shape) on a grid.
    """
    # Create two circle polygons
    circle1 = Point(cx1, cy1).buffer(radius, resolution=100)
    circle2 = Point(cx2, cy2).buffer(radius, resolution=100)
    # Union
    peanut_shape = circle1.union(circle2)
    # Get outline pixels
    pixels = []
    for x in range(grid_size):
        for y in range(grid_size):
            pt = Point(x, y)
            # Pixel is inside the peanut and at least one neighbor is outside (i.e., outline)
            if peanut_shape.contains(pt):
                if (
                    not peanut_shape.contains(Point(x-1, y)) or
                    not peanut_shape.contains(Point(x+1, y)) or
                    not peanut_shape.contains(Point(x, y-1)) or
                    not peanut_shape.contains(Point(x, y+1))
                ):
                    pixels.append({"x": x, "y": y})
    return pixels

def multi_circle_peanut_outline_pixels(
    grid_size=100,
    r_large=22, cx1=38, cy1=50, cx2=62, cy2=50,
    r_small=8, sx1=50, sy1=41, sx2=50, sy2=59
):
    """
    Returns a list of {"x": int, "y": int} dicts representing the outline
    of a peanut shape made from two large lobe circles and two small waist circles.
    """
    # Create four circle polygons
    circle1 = Point(cx1, cy1).buffer(r_large, resolution=100)
    circle2 = Point(cx2, cy2).buffer(r_large, resolution=100)
    small1 = Point(sx1, sy1).buffer(r_small, resolution=100)
    small2 = Point(sx2, sy2).buffer(r_small, resolution=100)
    # Union all
    peanut_shape = circle1.union(circle2).union(small1).union(small2)
    # Get outline pixels
    pixels = []
    for x in range(grid_size):
        for y in range(grid_size):
            pt = Point(x, y)
            if peanut_shape.contains(pt):
                if (
                    not peanut_shape.contains(Point(x-1, y)) or
                    not peanut_shape.contains(Point(x+1, y)) or
                    not peanut_shape.contains(Point(x, y-1)) or
                    not peanut_shape.contains(Point(x, y+1))
                ):
                    pixels.append({"x": x, "y": y})
    return pixels

@app.route("/peanut")
async def peanut_chart():
    peanut_pixels = multi_circle_peanut_outline_pixels()
    # Pass peanut_pixels to the template
    return await render_template("peanut_chart.html", peanut_pixels=json.dumps(peanut_pixels))

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
