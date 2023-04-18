from dataclasses import dataclass, asdict
from os import path, environ

#path.dirname(상위 디렉토리로 올려줌), path.abspath(__file__) 현재 파일의 경로를 나타냄
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))));

@dataclass #dict 자료형으로 보기 위한 것
class Config:
    """
    기본 Configuration
    """

    BASE_DIR = base_dir

    DB_POOL_RECYCLE:int = 900
    DB_ECHO:bool = True

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD:bool = True

@dataclass #dict형태로 보고 싶기 때문이라고 하는데..
class ProdConfig(Config):
    PROJ_RELOAD:bool = False 

# def abc(DB_ECHO:None, DB_POOL_RECYCLE:None, **kwargs):
#     print(DB_ECHO, DB_POOL_RECYCLE);
# args = asdict(LocalConfig());
# print(args)
# print(abc(**args)) ;

def conf():
    """
        환경 불러오기
    """
    config = dict(prod=ProdConfig(), local=LocalConfig());
    print("config", config)
    return config.get(environ.get("API_ENV", "local"));

