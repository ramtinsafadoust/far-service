from flask import Flask,redirect,request,flash,session,url_for
from flask_sqlalchemy  import SQLAlchemy
from flask import render_template
import secrets
import random
import jdatetime
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user



app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///devices.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
jdatetime.set_locale('fa_IR')


Login_manager= LoginManager()
Login_manager.init_app(app)





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
    repair_report=db.Column(db.String(400))


    def __repr__ (self):
        return f"devices('{self.tracking_number}','{self.customer_name}','{self.customer_phone}','{self.device_type}','{self.device_model}','{self.serial_number}','{self.property_number}','{self.address}','{self.problem}','{self.accesories}','{self.other_text}','{self.giver_name}','{self.in_time}','{self.out_time}','{self.situation}','{self.deliverd}')"



class users(UserMixin,db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(100))
    surename=db.Column(db.String(100))
    level=db.Column(db.Integer)


    def __repr__(self):
        return f"devices('{self.username}','{self.password}','{self.surename}','{self.level}')"


@Login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


@app.route('/')

def home():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
   



    return render_template("index.html",values=devices.query.all())



@app.route('/out', methods=["POST","GET"])
def out():
    if request.method=='POST':
        if request.form['yes']=="yes":
            return "ok"

    return render_template('index.html')



@app.route('/login',methods=["POST","GET"])
def login():

    if request.method=='POST':
        usernameform=request.form["username"]
        passwordform=request.form["password"]

        user =users.query.filter_by(username=usernameform,password=passwordform).first() 
        #print (user)
        #return str(user) 
        if user!=None:
            login_user(user)
            return redirect(url_for('home'))   
        else:
            return render_template("login.html",khata="نام کاربری و یا گذرواژه صحیح نمیباشد")

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('login'))

def listtostrint(s):
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele
       # str1 =str1+"  -  " 
    
    # return string   
    return str1  

@app.route('/edit',methods=['POST','GET'])
def edit():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    if request.method=='POST':
        id=request.form["idd"]
        print(id)
        dev =devices.query.filter_by(_id=id).first()
        #fname=dev.customer_name
       

    return render_template('edit.html',dev=dev)


@app.route('/edited',methods=['POST','GET'])
def edited():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    if request.method=="POST":
        
        #print(request.form.getlist("accessories"))
        id=request.form["id"]
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

        
        dev =devices.query.filter_by(_id=id).first()
        dev.tracking_number=tracking_number
        dev.customer_name=customer_name
        dev.customer_phone=customer_phone
        dev.device_type=device_type
        dev.device_model=device_model
        dev.serial_number=serial_number
        dev.property_number=property_number
        dev.address=address
        dev.problem=problem
        dev.accesories=accesories
        dev.other_text= other_text
        dev.in_time=in_time

                
        db.session.commit()

    return redirect(url_for('home'))



@app.route('/report' ,methods=['POST','GET'])
def report():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    if request.method=='POST':
        id=request.form["idd"]
        report=request.form["report"]
        st=(listtostrint(request.form.getlist("st")))
        device=devices.query.filter_by(_id=id).first()
        device.repair_report=report
        device.situation=st
        db.session.commit()

        return redirect(url_for("home"))
    return "report"

@app.route('/deliver',methods=['POST','GET'])
def deliver():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    if request.method=='POST':
        id=request.form["iddd"]
        device=devices.query.filter_by(_id=id).first()
        device.deliverd=1
        device.out_time=jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
        db.session.commit()
        return redirect(url_for("home"))
    return "ok"

@app.route('/archive',methods=['POST','GET'])
def archive():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

        
    values=devices.query.all()


    return render_template('archive.html',values=values)
        


@app.route('/add',methods=["POST","GET"])
def add():
    jdatetime.set_locale('fa_IR')
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    print(jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
    regby=current_user.surename
    if request.method=="POST":
        
        #print(request.form.getlist("accessories"))
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
        in_time=jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

       #in_time=request.form["in_time"]
       # out_time=request.form["out_time"]
        newone=devices(tracking_number=tracking_number,customer_name=customer_name,customer_phone=customer_phone,device_type=device_type,device_model=device_model,serial_number=serial_number,property_number=property_number,address=address,problem=problem,other_text=other_text,giver_name=giver_name,in_time=in_time,out_time='',situation=situation,deliverd=deliverd,accesories=accesories)
        db.session.add(newone)
        db.session.commit()
        return redirect('/')
    else:
        pass
    return render_template('add.html',time=jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"),regby=regby)




if __name__ == '__main__':
    
    
    app.run()