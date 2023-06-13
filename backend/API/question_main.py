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
        answer = request.form.get("answer",None,type="str")
        
        if(title is None) or (explanation is None) or (answer is None) or (title =="") or (explanation =="") or (answer ==""):
            raise TextPostValueError("タイトルと説明と答えを入力してください")
        
        if len(title) >20:
            raise TextPostValueError("タイトルの文字数が20文字を超えています")
        
        if len(explanation) > 30:
            raise TextPostValueError("説明の文字数が30文字を超えています")
        
        if len(answer) > 256:
            raise TextPostValueError("答えの文字数が256文字を超えています")
        
        session = DB.create_session()
        question_data = DB.Question_data(
            title=title,
            explanation=explanation
        )
        session.add(question_data)
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
def get_data_data():
    try:
        session = DB.create_session()
        questions_data = session.query(DB.Question_data).all()
        return jsonify([question_data.to_dict() for question_data in questions_data])
    except:
        return jsonify([]), 500

@api_module.route("/question/<int:_id>")
def get_question(_id):
    try:
        session = DB.create_session()
        question_data = session.query(DB.Question_data).filter(DB.Question_data.id == _id).first()
        if question_data is None:
            raise QuestionNotFoundError("問題が存在しません")
        
        return jsonify({
            "result": True,
            "question": question_data.to_dict() 
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
        answer = request.form.get("answer",None,type=str)
        _id = request.form.get("id",None,type=int)
        
        if _id is None:
            raise TextPostValueError("idを入力してください")
        
        if (title is None) and (explanation is None) or (answer is None) or (title =="") or (explanation =="") or (answer ==""):
            raise TextPostValueError("タイトルと説明と答えを入力してください")
        
        if title:
            if len(title) > 20:
                raise TextPostValueError("タイトルの文字数が20文字を超えています")
        
        if len(explanation) > 30:
            raise TextPostValueError("説明の文字数が30文字を超えています")
        
        if len(answer) > 256:
            raise TextPostValueError("答えの文字数が256文字を超えています")
        
        session = DB.create_session()
        question_data = session.query(DB.Question_data).filter(DB.Question_data.question.id == _id).first()
        if question_data is None:
            raise TextPostValueError("問題がありません")
        
        if title:
            question_data.title = title
        if explanation:
            question_data.explanation = explanation
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
        question_data = session.query(DB.Question_data).filter(DB.Question_data.question.id == _id).first()
        if question_data is None:
            raise TextPostValueError("問題がありません")
        
        session.delete(question_data)
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