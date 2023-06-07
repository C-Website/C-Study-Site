import os
import sys
from flask import jsonify,Blueprint,request

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import database as DB

api_module = Blueprint("main",__name__,url_prefix="/main")

class TextPostValueError(Exception):
    pass
class TextNotFoundError(Exception):
    pass

@api_module.route("",methods=["POST"])
def main():
    try:
        title = request.form.get("title",None,type="str")
        explanation = request.form.get("explanation",None,type="str")
        
        if(title is None) or (explanation is None) or (title =="") or (explanation ==""):
            raise TextPostValueError("タイトルと説明を入力してください")
        
        if len(title) >20:
            raise TextPostValueError("タイトルの文字数が20文字を超えています")
        
        if len(explanation) > 30:
            raise TextPostValueError("説明の文字数が30文字を超えています")
        
        session = DB.create_session()
        question_main = DB.Question_main(
            title=title,
            explanation=explanation
        )
        session.add(question_main)
        session.commit()
        
        return jsonify({
            "result":True
        })
    except TextPostValueError as e:
        print(e)
        return jsonify({
            "result":False,
            "message":e.args[0]
        })
    except  Exception as e:
        print(e)
        return jsonify({
            "result":False,
            "message":"Internal Server Error"
        }), 500
        