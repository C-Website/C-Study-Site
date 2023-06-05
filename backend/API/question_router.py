from flask import Blueprint
from API import question_main

question = Blueprint("question",__name__, url_prefix="/question")
api_modules = [question_main.api_module]

for module in api_modules:
    question.register_blueprint(module)