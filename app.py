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
    page = request.args.get('page', 1, type=int)  # par defaut 1
    #variable depenses pour listes les depenses par ordre 
    depenses = Depense.query.order_by(Depense.titre).paginate(page=page, per_page=5, error_out=False)
    page = request.args.get('page', 1, type=int)
    revenus = Revenu.query.order_by(Revenu.titre).paginate(page=page, per_page=5, error_out=False)

    #calcul de la somme des depenses on récupère tout les dep puis on util la fonc sum pour faire la somme 
    # et scalar() pour renvoyer une seule valeur
    total_deps = db.session.query(db.func.sum(Depense.montant)).scalar()
    budget = db.session.query(db.func.sum(Revenu.montant)).scalar()
    solde = total_deps - budget

    return render_template("index.html",total_deps=total_deps, depenses=depenses, revenus=revenus, budget=budget, solde=solde)

#index pour depense
@app.route("/depense")
def index_depense():
   
    return render_template("depense/index_depense.html")

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
            
            return redirect("/")
        except Exception:
            return "erreure "
    else:
        flash("Ajout fait avec success", "success")
        redirect("/")

    return render_template("depense/create_depense.html")


@app.route("/delete/<int:id>/")
def delete(id):
    
    depenses = Depense.query.get_or_404(id)
    try:
        db.session.delete(depenses)
        db.session.commit()
        flash("La supression a reussi !!", "danger")
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
            flash("La modification a reussi !!")
            return redirect("/")
        except Exception:
            print("erreur")
    
    return render_template("depense/update.html", depense=depense)

################################################
#la classe revenu creation des tables
class Revenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Gestion_budget: {self.titre, self.montant}"

#index revenu
@app.route("/revenu")
def index_revenu():

    return render_template("revenu/index_revenu.html")

#supprimer revenu
@app.route("/delete_revenu/<int:id>/")
def delete_revenu(id):
    revenus = Revenu.query.get_or_404(id)
    try:    
        db.session.delete(revenus)
        db.session.commit()
        return redirect("/")
    except Exception:
        print("invalid")

#ajouter revenu
@app.route("/create_revenu", methods=["GET", "POST"])
def create_revenu():
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        try:
            rev=Revenu(titre=titre, montant=montant)
            db.session.add(rev)
            db.session.commit()
            return redirect("/")
        except Exception:
            print("une s'est produite")
        
    return render_template("revenu/create_revenu.html")

if __name__ == "__main__":
    app.run(debug=True)