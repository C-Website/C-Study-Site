import os
import sys
from flask import jsonify,Blueprint,request

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import database as DB

api_module = Blueprint("main",__name__,url_prefix="/main")

class TextPostValueError(Exception):
    pass
class QuestionNotFoundError(Exception):
    pass

@api_module.route("/post",methods=["POST"])
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

@api_module.route("/questions")
def get_main_data():
    try:
        session = DB.create_session()
        questions_main = session.query(DB.Question_main).all()
        return jsonify([question_main.to_dict() for question_main in questions_main])
    except:
        return jsonify([]), 500

@api_module.route("/question/<int:_id>")
def get_question(_id):
    try:
        session = DB.create_session()
        question_main = session.query(DB.Question_main).filter(DB.Question_main.id == _id).first()
        if question_main is None:
            raise QuestionNotFoundError("問題が存在しません")
        
        return jsonify({
            "result": True,
            "question": question_main.to_dict() 
        })
    except QuestionNotFoundError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "問題が存在しません"
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500
        
@api_module.route("/update",methods=["POST"])
def update():
    try:
        title = request.form.get("title",None,type=str)
        explanation = request.form.get("explanation",None,type=str)
        _id = request.form.get("id",None,type=int)
        
        if _id is None:
            raise TextPostValueError("idを入力してください")
        
        if (title is None) and (explanation is None) or (title == "") and (explanation == "") and (explanation == ""):
            raise TextPostValueError("タイトルと説明を入力してください")
        
        if title:
            if len(title) > 20:
                raise TextPostValueError("タイトルの文字数が20文字を超えています")
        
        session = DB.create_session()
        question_main = session.query(DB.Question_main).filter(DB.Question_main.question.id == _id).first()
        if question_main is None:
            raise TextPostValueError("問題がありません")
        
        if title:
            question_main.title = title
        if explanation:
            question_main.explanation = explanation
        session.commit()
        
        return jsonify({
            "result":True
        })
    except TextPostValueError as e:
        print(e)
        return jsonify({
            "result":False,
            "message": e.args[0]
        }), 400
    except QuestionNotFoundError as e:
        print(e)
        return jsonify({
            "result":False,
            "message": e.args[0]
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result":False,
            "message": "Internal Server Error"
        }), 500
        
@api_module.route("/delete",methods=["DELETE"])
def delete():
    try:
        _id = request.form.get("id", None, type=int)
        
        if _id is None:
            raise TextPostValueError("idを入力してください")
        
        session = DB.create_session()
        question_main = session.query(DB.Question_main).filter(DB.Question_main.question.id == _id).first()
        if question_main is None:
            raise TextPostValueError("問題がありません")
        
        session.delete(question_main)
        session.commit()
        
        return jsonify({
            "result": True
        })
    except TextPostValueError as e:
        print(e)
        return jsonify({
            "result":False,
            "message": e.args[0]
        }), 400
    except QuestionNotFoundError as e:
        print(e)
        return jsonify({
            "result":False,
            "message": e.args[0]
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result":False,
            "message": "Internal Server Error"
        }), 500