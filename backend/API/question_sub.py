import os
import sys
from flask import jsonify,Blueprint,request

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import database as DB
api_module = Blueprint("sub",__name__,url_prefix="/sub")

def sub(question_sub_table):
    # Question_sub
    question_sub_data = {}
    for sub_data in question_sub_table:
        add_sub_data = {
            "title": sub_data.title,
            "answer": sub_data.answer
        }
        question_sub_data[str(sub_data.id)] = add_sub_data
        
@api_module.route("",methods=['GET'])
def sub():
    try:
        session = DB.create_session()
        question_sub_data = session.query(DB.Question_main,DB.Question_sub)\
            .join(DB.Question_sub,DB.Question_main.id == DB.Question_sub.id).all()
            
        return jsonify({
            "result": True,
            "data": sub(question_sub_data)
        })
        
    except Exception as e:
        print(e)
        return jsonify({
            "resullt": False,
            "message": "Internal Server Error"
        }), 500
                                          