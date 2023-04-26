import contextlib

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#프로젝트 루트 디렉토리에 저장한다. 
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

#커넥션 풀 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#데이터베이스 접근에 필요한 클래스, autocommit, autoflush True일 경우 데이터가 반영되면 바로 저장된다.
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()