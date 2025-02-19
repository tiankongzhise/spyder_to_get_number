from sqlalchemy import create_engine, Column, String, Integer, Date,DateTime,UniqueConstraint,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from zoneinfo import ZoneInfo



Base = declarative_base()

def beijing_time():
    # 创建北京时区对象
    beijing_tz = ZoneInfo("Asia/Shanghai")
    # 获取当前北京时间
    now = datetime.now(beijing_tz)

    return now.date()

class AdmissionRecordTable(Base):
    __tablename__ = 'admission_records'

   

    
    # 修改为自增主键（需注意数据库兼容性）
    logic_key = Column(
        Integer, 
        primary_key=True,
        autoincrement=True,  # 启用自增
        comment='自增逻辑主键',
        # 如果使用PostgreSQL需要显式序列：
        # server_default=Sequence('logic_key_seq').next_value()
    )
    id = Column(String(32), comment='不知道是啥')
    yxdm = Column(String(10), comment='院校代码')
    yxmc = Column(String(50), comment='院校名称')
    yxdh = Column(String(20), nullable=True, comment='院校电话')
    jhlbdm = Column(String(10), comment='计划类别代码')
    jhlbmc = Column(String(50), comment='计划类别名称')
    zydh = Column(String(10), comment='专业代码')
    zyxh = Column(String(10), comment='专业序号')
    zymc = Column(String(50), comment='专业名称')
    zyzmc = Column(String(50), comment='专业组名称')
    zyzbh = Column(String(10), comment='专业组编号')
    kslbmc = Column(String(50), nullable=True, comment='考生类别名称')
    zyrsy = Column(Integer, comment='专业剩余人数')
    tjjzsj = Column(DateTime, comment='统计截止时间')
    dm = Column(String(20), nullable=True, comment='代码')
    record_date = Column(Date, default=beijing_time,nullable=False,comment='记录时间')

    # 唯一索引配置
    __table_args__ = (
        UniqueConstraint(
            'record_date', 
            'yxdm',
            'zydh',
            'jhlbdm',
            name='uq_record_date_yxdm_zydh_jhlbdm'
        ),
        {'comment': '唯一索引'}
    )


class MajorTable(Base):
    __tablename__ = 'majors'  # 表名根据实际需求修改
    table_key = Column(Integer, primary_key=True, autoincrement=True)
    zyzdm = Column(String(20))                   # 专业组代码
    zydm = Column(String(20))                    # 专业代码
    zymc = Column(String(50))                    # 专业名称
    yxdh = Column(String(10))                    # 院系代号
    zydh = Column(String(10))                    # 专业代号
    jhrs = Column(Integer)                       # 计划人数
    xzdm = Column(String(10))                    # 学制代码
    skkmyq = Column(String(50))                  # 省控科目要求
    wyyzdm = Column(String(50))                  # 外语语种代码
    sfbz = Column(String(10))                    # 省份标准
    kskmyq = Column(String(50))                  # 考生科目要求
    sfks = Column(Boolean)                       # 是否考试
    bxddbb = Column(Boolean)                     # 是否需要报备
    bz = Column(String(500))                     # 备注
    record_date = Column(Date, default=beijing_time,nullable=False,comment='记录时间')
    # 唯一索引配置
    __table_args__ = (
        UniqueConstraint(
            'record_date', 
            'yxdh',
            'zyzdm',
            'zydm',
            'zydh',
            name='uq_record_date_yxdh_zyzdm_zydm'
        ),
        {'comment': '唯一索引'}
    )

class MajorPlanTable(Base):
    __tablename__ = 'majors_plan'  # 表名根据实际需求修改
    table_key = Column(Integer, primary_key=True, autoincrement=True)
    zyzdm = Column(String(20))                   # 专业组代码
    zydm = Column(String(20))                    # 专业代码
    zymc = Column(String(50))                    # 专业名称
    yxdh = Column(String(10))                    # 院系代号
    zydh = Column(String(10))                    # 专业代号
    jhrs = Column(Integer)                       # 计划人数
    xzdm = Column(String(10))                    # 学制代码
    skkmyq = Column(String(50))                  # 省控科目要求
    wyyzdm = Column(String(50))                  # 外语语种代码
    sfbz = Column(String(10))                    # 省份标准
    kskmyq = Column(String(50))                  # 考生科目要求
    sfks = Column(Boolean)                       # 是否考试
    bxddbb = Column(Boolean)                     # 是否需要报备
    bz = Column(String(500))                     # 备注
    record_date = Column(Date, default=beijing_time,nullable=False,comment='记录时间')
    # 唯一索引配置
    __table_args__ = (
        UniqueConstraint(
            'record_date', 
            'yxdh',
            'zyzdm',
            'zydm',
            'zydh',
            name='uq_record_date_yxdh_zyzdm_zydm'
        ),
        {'comment': '唯一索引'}
    )


# 数据库配置（根据实际情况修改）
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
}

# 创建数据库引擎
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"
)

# 创建数据表（如果不存在）
Base.metadata.create_all(engine)

# 创建会话工厂
Session = sessionmaker(bind=engine)