from flask import Flask, render_template


app = Flask(__name__)

solutionEdgeId = 1
def getId():
    global solutionEdgeId
    newId = solutionEdgeId
    solutionEdgeId += 1
    return newId

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

 


# label style => step number +  node name + cost spent until now + remaining cost + total cost
    solutionEdges = {
        "id": getId(),
        "label":"1. S 0-17-17",
        "children":[
            {
                "id": getId(),
                "label":"2. A 6-10-16",
                "children":[
                    {
                        "id": getId(),
                        "label":"4. A 12-4-16",
                    }
                ]
            },
            {
                "id": getId(),
                "label":"2. C 10-4-14",
                "children":[
                    {
                        "id": getId(),
                        "label":"3. D 16-2-18",
                    }
                ]
            },
            {
                "id": getId(),
                "label":"2. B 5-13-18",
                "children":[
                    {
                        "id": getId(),
                        "label":"7. E 10-4-15",
                    },
                    {
                        "id": getId(),
                        "label":"7. D 12-2-14",
                    }
                ]
            }
        ]
    }

    bestPath = ["S 0-17-17", "A 10-2-14", "B 12-5-17", "C 13-3-16", "G 18-1-18"]

    return render_template("index.html", nodes=nodes, edges=edges, solutionEdges=solutionEdges, bestPath=bestPath)


if __name__ == "__main__":
    app.run(debug=True)
