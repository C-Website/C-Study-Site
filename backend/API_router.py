from flask import Blueprint
from API.question_router import question

api = Blueprint("API", __name__,url_prefix="/api")
api.register_blueprint(question)