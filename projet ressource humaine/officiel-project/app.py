from flask import Flask,render_template,request,session,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy

messageee = ''
message = ''
messagge = ''
sea = ''
dell=''

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'LISDJHVUIOEDNHVEUKDHVUIERNHUIWEKLMCV'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'

class Employer(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)   
    CIN = db.Column(db.String(30), nullable=False , unique=True)
    adresss = db.Column(db.String(30), nullable=False)
    Email = db.Column(db.String(30), nullable=False)
    tele = db.Column(db.String(30), nullable=False)
    travail = db.Column(db.String(30), nullable=False)
    grade = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(30),nullable = False )

    def __init__(self , nom , prenom , CIN , adresss , Email, tele , travail,grade,date,image):       
        self.nom = nom
        self.prenom = prenom
        self.CIN = CIN
        self.adresss = adresss 
        self.Email = Email
        self.tele = tele
        self.travail = travail
        self.grade = grade
        self.date = date
        self.image = image






@app.route('/home', methods=['POST','GET'])
def home():
    return render_template('home.html' , title='home')

@app.route('/',  methods=['POST','GET'])
def login():
    global messageee
    if request.method == 'POST':
        session['email'] = request.form.get('email')
        session['password'] = request.form.get('password')
        if session['email'] == 'oussama@gmail.com' and session['password'] == '1234':
            return render_template('home.html',title = 'HOME ')
        else:
            messageee = 'Invalid Email ou mot de passe'
            return redirect(url_for('login'))
    return render_template('login.html',messageee=messageee ,title = 'Login')


@app.route('/add' ,methods=['POST','GET'])
def add():
    if request.method == 'POST':
        name= request.form.get('name')
        fname= request.form.get('fname')
        cin= request.form.get('cin')
        adress= request.form.get('adress')
        email= request.form.get('email')
        number= request.form.get('number')
        job= request.form.get('job')
        grade= request.form.get('grade')
        date= request.form.get('date')
        picture= request.form.get('image')
        data = Employer(name , fname ,cin ,adress,email,number,job,grade,date,picture)
        flash('lempleyer est bien ajouter','success')
        db.session.add(data)
        db.session.commit()

        return redirect(url_for('details'))
    return render_template('add.html',title = 'Ajouter')
    
@app.route('/find' , methods=['POST','GET'])
def find():
    global messagge,sea
    if request.method == 'POST':
        session['find'] = request.form.get('find')
        dataa  = Employer.query.filter_by(CIN =session['find']).first()
        if dataa:
            messagge = dataa
            redirect(url_for('find'))
        else:
            messagge   =  'not found'
            redirect(url_for('find')) 


    all_data = Employer.query.all()
    return render_template('find.html' , mydata = all_data , messagge = messagge  , res = sea,title = 'Trouver')
    

@app.route('/delete/', methods = ['GET', 'POST'])
def delete():
        global message,dell
        if request.method == 'POST':
            session['CIN'] = request.form.get('ciin')
            cin = Employer.query.filter_by(CIN =session['CIN']).first()
            if cin:
                dell = cin
                redirect(url_for('delete'))
            else:
                message = 'not found'
                redirect(url_for('delete'))
        return render_template('delete.html',message=message,dell= dell,title = 'Suprimer')

@app.route('/suprimer/<id>/', methods = ['GET', 'POST'])
def supprimer(id):
    global dell
    dat = Employer.query.get(id)
    db.session.delete(dat)
    db.session.commit()
    dell = ''
    flash("l'employé est supprimé",'warning')
    return render_template('delete.html')




@app.route('/clear', methods = ['GET', 'POST'])
def cleear():
     global messagge
     messagge = ''
     return redirect(url_for('find')) 

@app.route('/clearr', methods = ['GET', 'POST'])
def cleearr():
     global sea,message,dell
     sea = ''
     message = ''
     dell=''
     return redirect(url_for('delete'))


@app.route('/clearrr')
def cleearrr():
     global sea,message,dell
     sea = ''
     message = ''
     dell=''
     return redirect(url_for('delete'))



@app.route('/employedetails')
def details():
    all_data = Employer.query.all()
    return render_template('employedet.html',mydata=all_data)
    
@app.route('/modifier', methods = ['GET', 'POST'])
def modifier():
    if request.method == "POST":
        data = Employer.query.get(request.form.get('id'))
        data.CIN = request.form['cin']
        data.nom = request.form['nom']
        data.prenom = request.form['prenom']
        data.Email = request.form['email']
        data.service = request.form['service']
        data.tele = request.form['num']
        data.adresss = request.form['adress']
        data.date = request.form['date']
        data.grade = request.form['grade']
        data.image = request.form['image']
        db.session.commit()
        flash("les données de l'employée ont été modifiées")
        return redirect(url_for('find'))



if __name__ == '__main__':
    app.run(debug=True,port=7050)

