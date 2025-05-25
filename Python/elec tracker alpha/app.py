from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculate_bill():
    total_cost = None
    if request.method == "POST":
        prev_reading = float(request.form["prev_reading"])
        curr_reading = float(request.form["curr_reading"])
        cost_per_kwh = float(request.form["cost_per_kwh"])

        consumption = curr_reading - prev_reading
        total_cost = consumption * cost_per_kwh

    return render_template("index.html", total_cost=total_cost)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
