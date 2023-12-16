from flask import Blueprint,render_template
from app.posts.forms import SearchForm

errors = Blueprint('errors',__name__)

@errors.context_processor
def basde():
    form=SearchForm()
    return dict(form=form)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'),404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'),403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'),500

#errorhandler is only for that particular route
#app_errorhandler can be used by all 
