from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

accounts = {
    "Conto Corrente": {
        "Casa": [],
        "Lavoro": []
    },
    "Carta Prepagata": {
        "Spese": [],
        "Viaggi": []
    }
}

@app.route("/")
def index():
    return render_template("index.html", accounts=accounts)

@app.route("/account/<name>")
def view_account(name):
    if name not in accounts:
        return "Conto non trovato", 404
    return render_template("account.html", account=name, categories=accounts[name])

@app.route("/account/<account>/category/<category>", methods=["GET", "POST"])
def view_category(account, category):
    if request.method == "POST":
        data = request.form["data"]
        descrizione = request.form["descrizione"]
        quantita = float(request.form["quantita"])
        transactions = accounts[account][category]
        saldo = transactions[-1]["saldo"] if transactions else 0
        saldo += quantita
        accounts[account][category].append({
            "data": data,
            "descrizione": descrizione,
            "quantita": quantita,
            "saldo": saldo
        })
        return redirect(url_for('view_category', account=account, category=category))
    return render_template("category.html", account=account, category=category, transactions=accounts[account][category])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
