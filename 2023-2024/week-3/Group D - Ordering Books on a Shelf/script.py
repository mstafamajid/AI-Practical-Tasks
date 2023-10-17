from flask import Flask, request, render_template
import math


app = Flask(__name__)


def permutation(n, r):
    if n >= r:
        return math.factorial(n) / math.factorial(n - r)
    else:
        return 0


import math


def generate_permutation_table(max_n, max_r):
    with open(
        "2023-2024\week-3\Group D - Ordering Books on a Shelf\solution.txt", "w"
    ) as file:
        for n in range(1, max_n + 1):
            for r in range(1, min(n, max_r) + 1):
                result = permutation(n, r)
                file.write(f"{n},{r},{result}\n")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        n = int(request.form["n"])
        r = int(request.form["r"])
        result = permutation(n, r)
        generate_permutation_table(n, r)
    return render_template("index.html", result=result)


@app.route("/permutation_table")
def permutation_table():
    table_data = []
    with open(
        "2023-2024\week-3\Group D - Ordering Books on a Shelf\solution.txt", "r"
    ) as file:
        for line in file:
            n, r, result = line.strip().split(",")
            table_data.append((n, r, result))
    return render_template("permutation_table.html", table_data=table_data)


if __name__ == "__main__":
    app.run(debug=False)
