from flask import Flask, render_template


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    nodes = {
        "s":{
            "row":0,
            "col":2,
            "cost":99
        },
        "a":{
            "row":2,
            "col":0,
            "cost":99
        },
        "b":{
            "row":2,
            "col":1,
            "cost":99
        },
        "c":{
            "row":2,
            "col":3,
            "cost":99
        },
        "e":{
            "row":4,
            "col":1,
            "cost":99
        },
        "d":{
            "row":4,
            "col":2,
            "cost":99
        },
        "f":{
            "row":5,
            "col":2,
            "cost":99
        },
        "g":{
            "row":6,
            "col":0,
            "cost":99
        },
    }

    edges = {
        "s-a":6,
        "s-b":5,
        "s-c":10,
        "a-e":6,
        "b-e":6,
        "b-d":7,
        "c-d":6,
        "e-f":4,
        "d-f":6,
        "f-g":3
    }
    return render_template("index.html", nodes=nodes, edges=edges)


if __name__ == "__main__":
    app.run(debug=True)
