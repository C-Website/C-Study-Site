import os
import sys
from flask import jsonify,Blueprint

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import database as DB

api_module = Blueprint("main",__name__,url_prefix="/main")

def create_question_main(question_main_table):
    question_main_data = {}
    for main_data in question_main_table:
        dict_main_data = main_data.to_dict()
        