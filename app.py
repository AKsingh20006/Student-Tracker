from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE = "students.json"


def load_students():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def save_students(students):
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)


@app.route("/")
def home():
    students = load_students()
    return render_template("index.html", students=students)


@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        students = load_students()

        students.append({
            "name": request.form["name"],
            "roll": request.form["roll"],
            "grades": {}
        })

        save_students(students)

        return redirect("/")

    return render_template("add_student.html")


@app.route("/add_grade", methods=["GET", "POST"])
def add_grade():

    students = load_students()

    if request.method == "POST":

        roll = request.form["roll"]
        subject = request.form["subject"]
        grade = request.form["grade"]

        for student in students:

            if student["roll"] == roll:
                student["grades"][subject] = float(grade)

        save_students(students)

        return redirect("/")

    return render_template("add_grade.html")


@app.route("/view_students")
def view_students():

    students = load_students()

    for student in students:

        grades = student["grades"].values()

        if grades:
            student["average"] = round(
                sum(grades) / len(grades), 2
            )
        else:
            student["average"] = 0

    return render_template(
        "view_students.html",
        students=students
    )


@app.route("/delete_student/<roll>", methods=["POST"])
def delete_student(roll):

    students = load_students()

    # keep every student whose roll does NOT match the one being deleted
    students = [s for s in students if s["roll"] != roll]

    save_students(students)

    return redirect("/view_students")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
