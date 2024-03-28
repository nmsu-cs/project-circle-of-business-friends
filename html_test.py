from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Hello, World!</title></head><body><h1>Hello, World!</h1><p>This is a test HTML page served by Flask.</p></body></html>'

if __name__ == '__main__':
    app.run(debug=True)