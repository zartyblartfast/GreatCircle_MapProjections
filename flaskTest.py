from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        with open('/home/zartyblartfast/test.txt', 'w') as f:
            f.write("Hello, World!")
        return 'File created successfully'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
