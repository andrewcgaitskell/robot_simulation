from quart import Quart, render_template

app = Quart(__name__)

@app.route('/')
async def hello():
    return {'message': 'Hello from Quart!'}

@app.route('/goodbye')
async def goodbye():
    return {'message': 'Goodbye from Quart!'}


@app.route('/health')
async def health():
    return {'status': 'healthy'}

@app.route('/chart')
async def chart():
    # Sample data for the 3D chart
    data = [
        {'x': 0, 'y': 5, 'z': 0, 'value': 10},
        {'x': 2, 'y': 3, 'z': 1, 'value': 15},
        {'x': -2, 'y': 7, 'z': -1, 'value': 20},
        {'x': 1, 'y': 2, 'z': 2, 'value': 12},
        {'x': -1, 'y': 6, 'z': -2, 'value': 18},
    ]
    return await render_template('chart.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
