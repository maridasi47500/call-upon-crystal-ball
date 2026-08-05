from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_gemplace", methods=["GET","POST"])
def add_one_gemplace():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into gemplace (lat,lon,name,description) values (:lat,:lon,:name,:description)",hey)
        user = query_db('select * from gemplace')

        return render_template("gemplaceform.html", gemplaces=user, one_user=one_user, the_title="add new gemplace")


    user = query_db('select * from gemplace')
    one_user = query_db("select * from gemplace limit 1", one=True)
    return render_template("gemplaceform.html", gemplaces=user, one_user=one_user, the_title="add new gemplace")

@app.route("/add_one_language", methods=["GET","POST"])
def add_one_language():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into language (name) values (:name)",hey)
        user = query_db('select * from language')

        return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")


    user = query_db('select * from language')
    one_user = query_db("select * from language limit 1", one=True)
    return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")

@app.route("/add_one_job", methods=["GET","POST"])
def add_one_job():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into job (name) values (:name)",hey)
        user = query_db('select * from job')

        return render_template("jobform.html", jobs=user, one_user=one_user, the_title="add new job")


    user = query_db('select * from job')
    one_user = query_db("select * from job limit 1", one=True)
    return render_template("jobform.html", jobs=user, one_user=one_user, the_title="add new job")

@app.route("/add_one_userhasjob", methods=["GET","POST"])
def add_one_userhasjob():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesjob= query_db("select * from job")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into userhasjob (job_id,user_id) values (:job_id,:user_id)",hey)
        user = query_db('select * from userhasjob')

        return render_template("userhasjobform.html", userhasjobs=user, one_user=one_user, the_title="add new userhasjob", touslesjob=touslesjob, touslesuser=touslesuser)


    touslesjob= query_db("select * from job")

    touslesuser= query_db("select * from user")

    user = query_db('select * from userhasjob')
    one_user = query_db("select * from userhasjob limit 1", one=True)
    return render_template("userhasjobform.html", userhasjobs=user, one_user=one_user, the_title="add new userhasjob", touslesjob=touslesjob, touslesuser=touslesuser)

@app.route("/add_one_programming_script", methods=["GET","POST"])
def add_one_programming_script():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into programming_script (lat,lon,title,description) values (:lat,:lon,:title,:description)",hey)
        user = query_db('select * from programming_script')

        return render_template("programming_scriptform.html", programming_scripts=user, one_user=one_user, the_title="add new programming_script")


    user = query_db('select * from programming_script')
    one_user = query_db("select * from programming_script limit 1", one=True)
    return render_template("programming_scriptform.html", programming_scripts=user, one_user=one_user, the_title="add new programming_script")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,password,phone,country_id) values (:username,:email,:password,:phone,:country_id)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','phone','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','phone','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','phone','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_post", methods=["GET","POST"])
def add_one_post():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        tousleslanguage= query_db("select * from language")

        one_user = query_db("insert into post (title,description,user_id,language_id) values (:title,:description,:user_id,:language_id)",hey)
        user = query_db('select * from post')

        return render_template("postform.html", posts=user, one_user=one_user, the_title="add new post", touslesuser=touslesuser, tousleslanguage=tousleslanguage)


    touslesuser= query_db("select * from user")

    tousleslanguage= query_db("select * from language")

    user = query_db('select * from post')
    one_user = query_db("select * from post limit 1", one=True)
    return render_template("postform.html", posts=user, one_user=one_user, the_title="add new post", touslesuser=touslesuser, tousleslanguage=tousleslanguage)

@app.route("/add_one_musicalscore", methods=["GET","POST"])
def add_one_musicalscore():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into musicalscore (time_signature,key_signature,title,content,user_id) values (:time_signature,:key_signature,:title,:content,:user_id)",hey)
        user = query_db('select * from musicalscore')

        return render_template("musicalscoreform.html", musicalscores=user, one_user=one_user, the_title="add new musicalscore", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from musicalscore')
    one_user = query_db("select * from musicalscore limit 1", one=True)
    return render_template("musicalscoreform.html", musicalscores=user, one_user=one_user, the_title="add new musicalscore", touslesuser=touslesuser)

@app.route("/add_one_sharewithgeniusmusicalscore", methods=["GET","POST"])
def add_one_sharewithgeniusmusicalscore():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesmusicalscore= query_db("select * from musicalscore")

        touslesjob= query_db("select * from job")

        touslesgemplace= query_db("select * from gemplace")

        one_user = query_db("insert into sharewithgeniusmusicalscore (musicalscore_id,description,job_id,gemplace_id) values (:musicalscore_id,:description,:job_id,:gemplace_id)",hey)
        user = query_db('select * from sharewithgeniusmusicalscore')

        return render_template("sharewithgeniusmusicalscoreform.html", sharewithgeniusmusicalscores=user, one_user=one_user, the_title="add new sharewithgeniusmusicalscore", touslesmusicalscore=touslesmusicalscore, touslesjob=touslesjob, touslesgemplace=touslesgemplace)


    touslesmusicalscore= query_db("select * from musicalscore")

    touslesjob= query_db("select * from job")

    touslesgemplace= query_db("select * from gemplace")

    user = query_db('select * from sharewithgeniusmusicalscore')
    one_user = query_db("select * from sharewithgeniusmusicalscore limit 1", one=True)
    return render_template("sharewithgeniusmusicalscoreform.html", sharewithgeniusmusicalscores=user, one_user=one_user, the_title="add new sharewithgeniusmusicalscore", touslesmusicalscore=touslesmusicalscore, touslesjob=touslesjob, touslesgemplace=touslesgemplace)

@app.route("/add_one_calluponaiprogrammingscript", methods=["GET","POST"])
def add_one_calluponaiprogrammingscript():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesprogramming_script= query_db("select * from programming_script")

        touslesjob= query_db("select * from job")

        touslesgemplace= query_db("select * from gemplace")

        one_user = query_db("insert into calluponaiprogrammingscript (programming_script_id,description,job_id,gemplace_id) values (:programming_script_id,:description,:job_id,:gemplace_id)",hey)
        user = query_db('select * from calluponaiprogrammingscript')

        return render_template("calluponaiprogrammingscriptform.html", calluponaiprogrammingscripts=user, one_user=one_user, the_title="add new calluponaiprogrammingscript", touslesprogramming_script=touslesprogramming_script, touslesjob=touslesjob, touslesgemplace=touslesgemplace)


    touslesprogramming_script= query_db("select * from programming_script")

    touslesjob= query_db("select * from job")

    touslesgemplace= query_db("select * from gemplace")

    user = query_db('select * from calluponaiprogrammingscript')
    one_user = query_db("select * from calluponaiprogrammingscript limit 1", one=True)
    return render_template("calluponaiprogrammingscriptform.html", calluponaiprogrammingscripts=user, one_user=one_user, the_title="add new calluponaiprogrammingscript", touslesprogramming_script=touslesprogramming_script, touslesjob=touslesjob, touslesgemplace=touslesgemplace)

@app.route("/add_one_sharepost", methods=["GET","POST"])
def add_one_sharepost():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslespost= query_db("select * from post")

        touslesjob= query_db("select * from job")

        touslesgemplace= query_db("select * from gemplace")

        one_user = query_db("insert into sharepost (user_id,post_id,description,job_id,gemplace_id) values (:user_id,:post_id,:description,:job_id,:gemplace_id)",hey)
        user = query_db('select * from sharepost')

        return render_template("sharepostform.html", shareposts=user, one_user=one_user, the_title="add new sharepost", touslesuser=touslesuser, touslespost=touslespost, touslesjob=touslesjob, touslesgemplace=touslesgemplace)


    touslesuser= query_db("select * from user")

    touslespost= query_db("select * from post")

    touslesjob= query_db("select * from job")

    touslesgemplace= query_db("select * from gemplace")

    user = query_db('select * from sharepost')
    one_user = query_db("select * from sharepost limit 1", one=True)
    return render_template("sharepostform.html", shareposts=user, one_user=one_user, the_title="add new sharepost", touslesuser=touslesuser, touslespost=touslespost, touslesjob=touslesjob, touslesgemplace=touslesgemplace)

