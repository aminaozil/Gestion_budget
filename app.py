from flask import Flask, redirect,render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
#configuration SQLAlchemy la base de données et le nom de la bd est gestion_app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gestion_budget.db"
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False

db = SQLAlchemy(app)

#la classe depense

class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Gestion_budget: {self.titre, self.montant}"

#liste page index pour depense
@app.route("/")
def index():
    depenses = Depense.query.order_by(Depense.titre)

    return render_template("index.html", depenses=depenses)

#create depense
@app.route("/create_dep", methods=["GET","POST"])
def create_dep():
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        dep = Depense(titre=titre,montant=montant)
        try:
            db.session.add(dep)
            db.session.commit()
            return redirect ("/")
        except Exception:
            return "erreure "
    else:
        redirect("/create_dep")

    return render_template("create_depense.html")


if __name__ == "__main__":
    app.run(debug=True)