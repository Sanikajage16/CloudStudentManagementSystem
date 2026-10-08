from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "cloudtask-secret-key"

# ==========================
# Database Connection
# ==========================

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    port=int(os.getenv("MYSQLPORT")),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE")
)

cursor = db.cursor()

# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("home.html")


# ==========================
# Register
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)",
            (fullname, email, password)
        )

        db.commit()

        return redirect("/login")

    return render_template("register.html")


# ==========================
# Login
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:

            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["email"] = user[2]

            return redirect("/dashboard")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# ==========================
# Dashboard
# ==========================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    # Total Courses
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    # Total Assignments
    cursor.execute("SELECT COUNT(*) FROM assignments")
    total_assignments = cursor.fetchone()[0]

    # Total Materials
    cursor.execute("SELECT COUNT(*) FROM materials")
    total_materials = cursor.fetchone()[0]

    # Average Attendance
    cursor.execute("SELECT AVG(percentage) FROM attendance")
    avg_attendance = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        total_courses=total_courses,
        total_assignments=total_assignments,
        total_materials=total_materials,
        avg_attendance=round(avg_attendance, 2)
    )


# ==========================
# Profile
# ==========================
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    return render_template("profile.html", user=user)

# ==========================
# Courses
# ==========================
@app.route("/courses")
def courses():

    if "user_id" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return render_template(
        "courses.html",
        courses=courses
    )

# ==========================
# Assignments
# ==========================
@app.route("/assignments")
def assignments():

    if "user_id" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()

    return render_template(
        "assignments.html",
        assignments=assignments
    )
# ==========================
# Attendance
# ==========================
@app.route("/attendance")
def attendance():

    if "user_id" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()

    return render_template(
        "attendance.html",
        attendance=attendance
    )
# ==========================
# Materials
# ==========================
@app.route("/materials")
def materials():

    if "user_id" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()

    return render_template(
        "materials.html",
        materials=materials
    )
# ==========================
# Logout
# ==========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==========================
# Run Application
# ==========================
if __name__ == "__main__":
    app.run(debug=True)