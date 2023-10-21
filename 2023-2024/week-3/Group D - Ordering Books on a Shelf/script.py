from flask import Flask, request, render_template

import os

# Specify the directory and file name
directory = "2023-2024/week-3/Group D - Ordering Books on a Shelf"
filename = "solution.txt"

# Create the absolute path
absolute_directory = os.path.abspath(directory)
absolute_path = os.path.join(absolute_directory, filename)

app = Flask(__name__)

dp = None  # permutation 2D matrix


# calculate permutation
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
        for row in dp:
            for element in row:
                file.write(f"{element},")
            file.write("\n")


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
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    matrix = []
    with open(absolute_path, "r") as file:
        for line in file:
            row = [x for x in line.strip().split(",")][:-1]
            matrix.append(row)

    # Calculate the total number of pages
    total_pages = (len(matrix) + per_page - 1) // per_page

    # Extract rows for the current page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    current_page_data = matrix[start_idx:end_idx]

    return render_template(
        "permutation_table.html",
        table_data=current_page_data,
        total_pages=total_pages,
        current_page=page,
    )


if __name__ == "__main__":
    app.run(debug=False)
