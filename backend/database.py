from sqlalchemy import create_engine,Column,Integer,Text,String
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

class Question_data(Base):
    
    __tablename__ = 'question_data'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    explanation = Column(String(30))
    answer = Column(String(256))
    
    def to_dict(self):
        question_data = {
            "id":self.id,
            "title":self.title,
            "explanation":self.explanation,
            "answer":self.answer
        }
        
        if self.explanation:
            question_data["explanation"] = self.explanation
        
        return question_data
    
    
def create_database():
    Base.metadata.create_all(bind=Engine)
    
def delete_database():
    Base.metadata.drop_all(bind=Engine)
    
def create_session():
    return sessionmaker(bind=Engine)()

if __name__ == "__data__":
    create_database