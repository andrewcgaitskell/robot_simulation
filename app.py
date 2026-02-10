from quart import Quart

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
