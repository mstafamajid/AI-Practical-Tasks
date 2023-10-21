from flask import Flask, request, render_template

import os

# Specify the directory and file name
directory = "2023-2024/week-3/Group D - Ordering Books on a Shelf"
filename = "solution.txt"

# Create the absolute path
absolute_directory = os.path.abspath(directory)
absolute_path = os.path.join(absolute_directory, filename)

app = Flask(__name__)

dp = None


def permutation(n, r):
    global dp
    if n >= r:
        dp = [[0] * (r + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            for j in range(min(i, r) + 1):
                if j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = dp[i - 1][j] + j * dp[i - 1][j - 1]
        return dp[n][r]
    else:
        return 0


def generate_permutation_table(max_n, max_r):
    with open(absolute_path, "w") as file:
        for n in range(1, max_n + 1):
            for r in range(1, min(n, max_r) + 1):
                result = dp[n][r]
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
    with open(absolute_path, "r") as file:
        for line in file:
            n, r, result = line.strip().split(",")
            table_data.append((n, r, result))
    return render_template("permutation_table.html", table_data=table_data)


if __name__ == "__main__":
    app.run(debug=False)