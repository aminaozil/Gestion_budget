from flask import Flask, flash, redirect,render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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

    page = request.args.get('page', 1, type=int)  # Default to page 1 if not specified
    #variable depenses pour listes les depenses par ordre 
    depenses = Depense.query.order_by(Depense.titre).paginate(page=page, per_page=5, error_out=False)
    #calcul de la somme des depenses on récupère tout les dep puis on util la fonc sum pour faire la somme 
    # et scalar() pour renvoyer une seule valeur
    total_deps = db.session.query(db.func.sum(Depense.montant)).scalar()

    return render_template("index.html", depenses=depenses, total_deps=total_deps)

#create depense
@app.route("/create_dep", methods=["GET","POST"])
def create_dep():
    error =None
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        dep = Depense(titre=titre,montant=montant)
        
        try:
            db.session.add(dep)
            db.session.commit()
            error="Ivalid"
            return redirect("/")
        except Exception:
            return "erreure "
    else:
        flash("Ajout fait avec success")
        redirect("/")

    return render_template("create_depense.html",error=error)


@app.route("/delete/<int:id>/")
def delete(id):
    
    depenses = Depense.query.get_or_404(id)
    try:
        db.session.delete(depenses)
        db.session.commit()
        return redirect("/")
    except Exception:
        
        print("une erreure s'est produite")

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    depense = Depense.query.get_or_404(id)
    if request.method == "POST":
        depense.titre = request.form['titre']
        depense.montant = request.form['montant']
        
        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            print("erreur")
    
    return render_template("update.html", depense=depense)

if __name__ == "__main__":
    app.run(debug=True)