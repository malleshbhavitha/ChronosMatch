
import csv
import io

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response,
)

from main import ChronosMatch


app = Flask(__name__)
app.secret_key = "chronosmatch-demo-key"

# One in-memory engine for this local demonstration.
engine = ChronosMatch()


@app.route("/")
def index():
    summary = engine.get_order_book_summary()
    trade_summary = engine.get_trade_summary()

    return render_template(
        "index.html",
        buy_orders=engine.buy_orders,
        sell_orders=engine.sell_orders,
        trades=engine.trade_history,
        summary=summary,
        trade_summary=trade_summary,
    )


@app.route("/add-order", methods=["POST"])
def add_order():
    try:
        order_type = request.form.get("order_type", "")
        price = float(request.form.get("price", ""))
        quantity_text = request.form.get("quantity", "")
        quantity = int(quantity_text)

        order_id = engine.add_order(order_type, price, quantity)

        flash(
            f"Order submitted successfully. Order ID: {order_id}",
            "success"
        )

    except (ValueError, TypeError):
        flash(
            "Please enter a valid order type, positive price, "
            "and positive whole-number quantity.",
            "error"
        )

    return redirect(url_for("index"))


@app.route("/cancel-order", methods=["POST"])
def cancel_order():
    try:
        order_id = int(request.form.get("order_id", ""))

        if engine.cancel_order(order_id):
            flash(f"Order {order_id} cancelled.", "success")
        else:
            flash(
                f"Pending order {order_id} was not found.",
                "error"
            )

    except (ValueError, TypeError):
        flash("Please enter a valid order ID.", "error")

    return redirect(url_for("index"))


@app.route("/download-trades")
def download_trades():
    output = io.StringIO()
    writer = csv.writer(output)

    # CSV column headings
    writer.writerow([
        "Trade No.",
        "Order Type",
        "Price",
        "Quantity",
        "Timestamp (UTC)"
    ])

    # Export all executed trades
    for number, trade in enumerate(engine.trade_history, start=1):
        writer.writerow([
            number,
            trade["incoming_order"],
            trade["price"],
            trade["quantity"],
            trade["timestamp"]
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=chronosmatch_trade_history.csv"
        }
    )


@app.route("/reset", methods=["POST"])
def reset():
    global engine

    engine = ChronosMatch()
    flash("Demo data has been reset.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
