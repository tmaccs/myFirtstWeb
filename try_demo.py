#encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import Users,Question,Answer
from exts import db
from decorator import login_restriction

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context={
        #'questions':Question.query.order_by('-create_time').all()
        'questions':Question.query.order_by('create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        user=Users.query.filter(Users.telephone==telephone,Users.password==password).first()
        if user:
            session['user_id']=user.id
            #return redirect(url_for('index'))
        #31天不删除，不需要再登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后登录'

@app.route('/logout/')
def logout():
    session.clear()
    #return redirect('login.html')
    return redirect(url_for('login'))

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        password=request.form.get('password')
        confirmPassword=request.form.get('confirmPassword')
    #手机号码验证，注册过了就不能注册了
        user=Users.query.filter(Users.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码'
        else:
            #判断确认密码和密码是否相等
            if confirmPassword != password:
                return u'两次密码不相同，请核对'
            else:
                user = Users(telephone=telephone,username=username,password=password)
                db.session.add(user)
                db.session.commit()
                #注册成功后，跳转到登录界面
                return redirect(url_for('login'))

#用了装饰器@login_restriction之后，question=login_restriction(question)=wrapper，因为装饰器中return的是wrapper
#run()这样运行就等于wrapper这样运行
@app.route('/question/',methods=['GET','POST'])
@login_restriction
def question():
    if request.method =='GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        # question = Question(title=title,content=content,author_name=user.username)
        question = Question(title=title, content=content)
        # 因为在login时，在session中保存了key为user_id的键值对，session['user_id']=user.id，所以：
        user_id = session.get('user_id')
        user = Users.query.filter(Users.id == user_id).first()
        question.author=user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
        question_detail=Question.query.filter(question_id==Question.id).first()
        return render_template('detail.html',question_d=question_detail)

@app.route('/addAnswer/',methods=['POST'])
@login_restriction
def addAnswer():
    content = request.form.get('answer_content')
    answer = Answer(content=content)

    user_id = session.get('user_id')
    user = Users.query.filter(Users.id == user_id).first()
    answer.author = user

    question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id==question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

@app.context_processor
def context_processor():
    #通过key来获得，所以是get('user_id')不是get('user.id')
    user_id = session.get('user_id')
    #如果User_id存在，则去数据库中找，从模型中拿出来
    if user_id:
        user = Users.query.filter(Users.id == user_id).first()
        if user:
            return {'user':user}
        else:
            return{}
    #这个return一定要写，不然会报TypeError: 'NoneType' object is not iterable
    return {}
if __name__ == '__main__':
    app.run()


