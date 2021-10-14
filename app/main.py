from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Python!"

@app.route("/username/<string:user>")
def user(user):
    return f"Hello from Python, {user}! "

@app.route("/id/<int:number>")
def numId(number):
    return f"Next number is {number+1}! "

if __name__ == "__main__":
    app.run(host='0.0.0.0')
