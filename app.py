from flask import Flask,redirect,request,flash,session
from flask_sqlalchemy  import SQLAlchemy
from flask import render_template
import secrets
import random
import jdatetime
from flask_login import LoginManager

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///devices.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
jdatetime.set_locale('fa_IR')






db = SQLAlchemy(app)

class devices(db.Model):
    _id= db.Column("id", db.Integer , primary_key=True)
    tracking_number =db.Column(db.String(100),nullable=False,unique=True)
    customer_name =db.Column(db.String(100),nullable=False)
    customer_phone =db.Column(db.String(20))
    device_type =db.Column(db.String(100))
    device_model =db.Column(db.String(100))
    serial_number =db.Column(db.String(100))
    property_number =db.Column(db.String(100))
    address =db.Column(db.String(300))
    problem =db.Column(db.String(500))
    accesories =db.Column(db.String(300))
    other_text =db.Column(db.String(700))
    giver_name =db.Column(db.String(100))
    in_time =db.Column(db.String(100))
    out_time =db.Column(db.String(100))
    situation=db.Column(db.Integer)
    deliverd=db.Column(db.Integer)


    def __repr__ (self):
        return f"devices('{self.tracking_number}','{self.customer_name}','{self.customer_phone}','{self.device_type}','{self.device_model}','{self.serial_number}','{self.property_number}','{self.address}','{self.problem}','{self.accesories}','{self.other_text}','{self.giver_name}','{self.in_time}','{self.out_time}','{self.situation}','{self.deliverd}')"



class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    pasword=db.Column(db.String(100))
    surename=db.Column(db.String(100))
    level=db.Column(db.Integer)


    def __repr__(self):
        return f"devices('{self.username}','{self.password}','{self.surename}','{self.level}')"




@app.route('/')
def home():


    return render_template("index.html",values=devices.query.all())





@app.route('/login',methods=["POST","GET"])
def login():

    #newone=devices(tracking_number='6763',customer_name='Ramtin Safadoust',customer_phone='09388826763',device_type='laptop',device_model='Lenovo Y700',serial_number='',property_number="",address='',problem='blue dead',accesories='adapter',other_text="",giver_name='Ali Vatani',in_time='dirooz',out_time='')
    #db.session.add(newone)
    #db.session.commit()
    return render_template("login.html")

def listtostrint(s):
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele + "-"
       # str1 =str1+"  -  " 
    
    # return string   
    return str1  


@app.route('/add',methods=["POST","GET"])
def add():
     
    if request.method=="POST":
       # print(request.form.getlist("accessories"))
        accs=(listtostrint(request.form.getlist("accessories")))
        #temp=request.form["customer_phone"]
        tracking_number=random.randint(1000000,9999999)
        customer_name=request.form["customer_name"]
        customer_phone=request.form["customer_phone"]
        device_type=request.form["device_type"]
        device_model=request.form["device_model"]
        serial_number=request.form["serial_number"]
        property_number=request.form["property_number"]
        address=request.form["address"]
        problem=request.form["problem"]
        accesories=accs
        other_text=request.form["other_text"]
        giver_name=request.form["giver_name"]
        situation=0
        deliverd=0
        in_time=request.form["in_time"]

       #in_time=request.form["in_time"]
       # out_time=request.form["out_time"]
        newone=devices(tracking_number=tracking_number,customer_name=customer_name,customer_phone=customer_phone,device_type=device_type,device_model=device_model,serial_number=serial_number,property_number=property_number,address=address,problem=problem,other_text=other_text,giver_name=giver_name,in_time=in_time,out_time='',situation=situation,deliverd=deliverd,accesories=accesories)
        db.session.add(newone)
        db.session.commit()
        return redirect('/')
    else:
        pass
    return render_template('add.html',time=jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))

if __name__ == '__main__':
    db.create_all()
    app.run()