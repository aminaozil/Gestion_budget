from flask import Flask, flash, redirect,render_template, request, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'flash message'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/gestion_budget"
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False

#configuration SQLAlchemy la base de données et le nom de la bd est gestion_app
db = SQLAlchemy(app)

class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_depense = db.Column(db.String(100), nullable=False)
    montant_depense = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Gestion_budget: {self.titre_depense, self.montant_depense}"

#liste page index pour depense
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/")
def index_depense():
    depenses = Depense.query.order_by(Depense.titre_depense)
   
    return render_template("/depense/index_depense.html", depenses=depenses)

#create depense
@app.route("/create_dep", methods=["GET","POST"])
def create_dep():

    if request.method == "POST":
        titre_depense = request.form['titre_depense']
        montant_depense = request.form['montant_depense']
        dep = Depense(titre_depense=titre_depense,montant_depense=montant_depense)
        
        try:
            db.session.add(dep)
            db.session.commit()
            flash("Ajout fait avec success", "success")
            return redirect("/")
        except Exception:
            return "erreure "
    else:
        
        redirect("/")

    return render_template("/depense/create_depense.html")

#supprimer depense
@app.route("/delete_depense/<int:id>/")
def delete_depense(id):
    
    depenses = Depense.query.get_or_404(id)
    try:
        db.session.delete(depenses)
        db.session.commit()
        flash("La supression a reussi !!")
        return redirect("/")
    except Exception:
        
        print("une erreure s'est produite")

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    depense = Depense.query.get_or_404(id)
    if request.method == "POST":
        depense.titre_depense = request.form['titre_depense']
        depense.montant_depense = request.form['montant_depense']
        
        try:
            db.session.commit()
            flash("La modification a reussi !!")
            return redirect("/")
        except Exception:
            print("erreur")
    
    return render_template("/depense/update.html", depense=depense)

if __name__ == "__main__":
    app.run(debug=True)