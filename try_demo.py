#encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session,g,flash
import config
from models import Users,Question,Answer
from exts import db
from decorator import login_restriction
from werkzeug.security import check_password_hash
from sqlalchemy import or_
import time

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context={
        #'questions':Question.query.order_by('-create_time').all()
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        #user=Users.query.filter(Users.telephone==telephone,Users.password==password).first()
        user=Users.query.filter(Users.telephone==telephone).first()
        if user and user.check_password(password):
            session['user_id']=user.id
            #return redirect(url_for('index'))
        #31天不删除，不需要再登录
            session.permanent = True
            flash("亲爱的，登录成功", 'success')
            # return redirect(url_for('login'))
            # time.sleep(1)
            return redirect(url_for('index'))
        else:
            flash("亲爱的，密码或者用户名不对!", 'danger')
            return redirect(url_for('login'))

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
            flash("亲爱的，手机号已存在!", 'danger')
            return redirect(url_for('register'))
        else:
            #判断手机号是否是11位
            if len(telephone)!= 11:
                flash("亲爱的，请输入11位手机号码!", 'danger')
                return redirect(url_for('register'))
            else:
                #判断确认密码和密码是否相等
                if confirmPassword != password:
                    flash("亲爱的，两次输入的密码不一样!", 'danger')
                    return redirect(url_for('register'))
                else:
                    user = Users(telephone=telephone,username=username,password=password)
                    db.session.add(user)
                    db.session.commit()
                    #注册成功后，跳转到登录界面
                    flash("亲爱的，注册成功，请登录", 'success')
                    time.sleep(1)
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
        # user_id = session.get('user_id')
        # user = Users.query.filter(Users.id == user_id).first()
        question.author=g.user
        #question.answer_num = Answer.query.filter(Question.id==Answer.id).last().id
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
        question_detail=Question.query.filter(Question.id==question_id).first()
        return render_template('detail.html',question_d=question_detail)

@app.route('/addAnswer/',methods=['POST'])
@login_restriction
def addAnswer():
    content = request.form.get('answer_content')
    answer = Answer(content=content)

    # user_id = session.get('user_id')
    # user = Users.query.filter(Users.id == user_id).first()
    answer.author = g.user

    question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id==question_id).first()

    answer.question = question

    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

@app.route('/buslines/')
def buslines():
    return render_template('buslines.html')

@app.route('/try_proj/')
def try_proj():

    return render_template('try_proj.html')

@app.route('/search/')
def search():
    q=request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains('q'),Question.content.contains('q')))
    return render_template('search.html',q=q,questions=questions)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    user = Users.query.filter(Users.id == user_id).first()
    g.user =user

@app.context_processor
def context_processor():
    #通过key来获得，所以是get('user_id')不是get('user.id')
    # user_id = session.get('user_id')
    # #如果User_id存在，则去数据库中找，从模型中拿出来
    # if user_id:
    #     user = Users.query.filter(Users.id == user_id).first()
    #     if user:
    if hasattr(g, 'user'):
            return {'user':g.user}
        #有这句话，折腾了两天，总是给我返回空字典，艹了
        # else:
        #     return{}
    #这个return一定要写，不然会报TypeError: 'NoneType' object is not iterable
    return {}
if __name__ == '__main__':
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()




