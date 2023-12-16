from flask import Blueprint,render_template,request
from app.models import Post,Question
from app.posts.forms import SearchForm


main = Blueprint('main',__name__)

@main.route('/main')
@main.route('/')
def index():
    #request.args.get is used to get the key value pair from teh arguement of the url
    page = request.args.get('page',1,type=int)  
    # the above is the arguemtn in the url
    #access the other page by ?page=2
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=7)
    questions = Question.query.order_by(Question.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template('index.html',posts = posts,questions=questions)

@main.route('/blog')
def blog():
    page = request.args.get('page',1,type=int)  
    # the above is the arguemtn in the url
    #access the other page by ?page=2
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=10)
    return render_template('blog.html',posts=posts)

@main.route('/QnA', methods=["POST", "GET"])
def QnA():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.order_by(Question.date_posted.desc()).paginate(page=page, per_page=10)
    form = SearchForm()
    if form.validate_on_submit():   
        searched = form.searched.data
        questions = Question.query.filter(Question.title.like('%' + searched + '%')) \
            .order_by(Question.date_posted.desc()) \
            .paginate(page=page, per_page=5)

    return render_template('QnA.html', form=form, questions=questions, searched=form.searched.data)



@main.route('/about')
def about():
    return render_template('about.html',title='about')


@main.context_processor
def base():
    form=SearchForm()
    return dict(form=form)