from sqlalchemy import DATE, Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(100), nullable=True, comment='国家')
    country_code = Column(String(100), nullable=True, comment='国家代码')
    country_pop = Column(BigInteger, nullable=True, comment='国家人口')
    data = relationship('Data', back_populates='city')  # Data 是关联类名， city 是反向查询字段名

    ts_created = Column(DateTime, server_default=func.now(), comment='创建时间')
    ts_updated = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {'order_by': country_code}  # 默认正序，倒序 desc

    def __repr__(self):
        return f'{self.country}_{self.province}'


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id')， comment='所属省/直辖市')  # ForeignKey('表名.字段名')
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    city = relationship('City', back_populates='data')
    
    __mapper_args__ = {'order_by': date.desc()}  # 默认正序，倒序 desc

    # repr() 函数将对象转化为供解释器读取的形式
    # 重写 __repr__ ， print(对象) 的时候直接转化
    def __repr__(self):
        return f'{repr(self.date)}: 确诊数 {self.confirmed}'


'''
SQLAlchemy 基本操作
http://www.taodudu.cc/news/show-175725.html

Python3 + SQLAlchemy + Sqlite3
http://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy 基础 Autoflush 和 Autocommit
https://zhuanlan.zhihu.com/p/48994990
'''