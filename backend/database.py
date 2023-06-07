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

class Question_main(Base):
    
    __tablename__ = 'question_main'
    
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer)
    title = Column(String(20))
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
    

class Question_sub(Base):
        
    __tablename__ = 'question_sub'
    
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, primary_key=True)
    example_question = Column(Text)
    main_question = Column(Text)
    code = Column(Text)
    
    def to_dict(self):
        question_sub = {
            "id": self.id,
            "genre_id": self.genre_id,
            "example_question": self.example_question,
            "main_question": self.main_question,
            "code": self.code
        }
    
        return question_sub

class Genre(Base):
    
    __tablename__ = 'genre'
    
    genre_id = Column(Integer, primary_key=True,autoincrement=True)
    question_genre = Column(Text)
    
    def to_dict(self):
        genre = {
            "genre_id": self.genre_id,
            "question_genre": self.question_genre
        }
        
        return genre
    
def create_database():
    Base.metadata.create_all(bind=Engine)
    
def delete_database():
    Base.metadata.drop_all(bind=Engine)
    
def create_session():
    return sessionmaker(bind=Engine)()

if __name__ == "__main__":
    create_database