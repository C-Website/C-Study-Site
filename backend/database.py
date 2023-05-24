from sqlalchemy import create_engine,Column,Integer,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path

db_folder = path.dirname(path.abspath(__file__))
db_path = path.join(db_folder, 'c-study.sqlite3')

DATABASE = 'sqlite:///{}'.format(db_path)

Engine = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo = False,
    connect_args={"check_same_thread": False}
)
Base = declarative_base()

class Question_main(Base):
    
    __tablename__ = 'question_main'
    
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer)
    title = Column(Text)
    explanation = Column(Text)
    
    def to_dict(self):
        question_main = {
            "id":self.id,
            "genre_id":self.genre_id,
            "title":self.title,
            "explanation":self.explanation
        }
        
        if self.explanation:
            question_main["explanation"] = self.explanation
            
        return question_main
    

class Exam_sentence(Base):
        
    __tablename__ = 'example'
    
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, primary_key=True)
    example_question = Column(Text)
    example_answer = Column(Text)
    
    def to_dict(self):
        exam_sentence = {
            "id": self.id,
            "genre_id": self.genre_id,
            "example_question": self.example_question,
            "example_answer": self.example_answer
        }
    
        return exam_sentence
    
class Text_body(Base):
    
    __tablename__ = "answer"
    
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, primary_key=True)
    text_question = Column(Text)
    text_answer = Column(Text)
    
    def to_dict(self):
        text_body = {
            "id": self.id,
            "genre_id": self.genre_id,
            "text_question": self.text_question,
            "text_answer": self.text_answer
        }
        
        return text_body
    
def create_database():
    Base.metadata.create_all(bind=Engine)
    
def delete_database():
    Base.metadata.drop_all(bind=Engine)
    
def create_session():
    return sessionmaker(bind=Engine)()

if __name__ == "__main__":
    create_database