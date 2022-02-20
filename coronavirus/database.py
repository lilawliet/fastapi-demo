import imp
import sqlite3


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABAASE_URL = 'sqlite:///./cornavirus.sqlite3'
# SQLALCHEMY_DATABAASE_URL = 'postgresql://username:password@host:port/database_name'  # postgresql

engine = create_engine(
    SQLALCHEMY_DATABAASE_URL,
    encoding='utf-8',
    # 引擎将用 repr() 函数记录语句及参数到日志
    echo=True,
    # 让任意线程可使用
    connect_args={'check_same_thread': False}
)

# SQLAlchemy 中 CRUD 是通过会话（session）进行， 每一个 SessionLocal 就是一个数据库 session
# flush()指发送数据库语句到数据库，但不一定执行写入磁盘
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)


# 创建映射类
Base = declarative_base(bind=engine, name='Base')