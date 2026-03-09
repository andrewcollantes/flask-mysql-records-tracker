from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# CONNECT TO MYSQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_Password",
    database="maintenance_tracker"
)

cursor = db.cursor(dictionary=True)


@app.route("/")
def index():
    search = request.args.get("search", "")

    if search:
        query = """
            SELECT * FROM records
            WHERE name LIKE %s OR category LIKE %s OR location LIKE %s
            ORDER BY id DESC
        """
        value = "%" + search + "%"
        cursor.execute(query, (value, value, value))
    else:
        cursor.execute("SELECT * FROM records ORDER BY id DESC")

    records = cursor.fetchall()
    return render_template("index.html", records=records, search=search)


@app.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        location = request.form["location"]
        reference_code = request.form["reference_code"]
        quantity = request.form["quantity"]
        status = request.form["status"]

        query = """
            INSERT INTO records (name, category, location, reference_code, quantity, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, category, location, reference_code, quantity, status))
        db.commit()

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_record(id):
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        location = request.form["location"]
        reference_code = request.form["reference_code"]
        quantity = request.form["quantity"]
        status = request.form["status"]

        query = """
            UPDATE records
            SET name=%s, category=%s, location=%s,
                reference_code=%s, quantity=%s, status=%s
            WHERE id=%s
        """
        cursor.execute(query, (name, category, location, reference_code, quantity, status, id))
        db.commit()

        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM records WHERE id=%s", (id,))
    record = cursor.fetchone()
    return render_template("edit.html", record=record)


@app.route("/delete/<int:id>")
def delete_record(id):
    cursor.execute("DELETE FROM records WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)