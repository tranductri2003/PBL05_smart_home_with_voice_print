from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
    
class Member(Base):
    __tablename__ = 'members_member'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)

    def __repr__(self):
        return f"<Member(id={self.id}, name={self.name}, about={self.about})>"

class Appliance(Base):
    __tablename__ = 'appliances_appliance'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"<Appliance(id={self.id}, name={self.name}, description={self.description})>"

class Permission(Base):
    __tablename__ = 'permissions_permission'
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members_member.id'))
    appliance_id = Column(Integer, ForeignKey('appliances_appliance.id'))

    member = relationship("Member")
    appliance = relationship("Appliance")

    def __repr__(self):
        return f"<Permission(member={self.member.name}, appliance={self.appliance.name})>"

# Đường dẫn đến CSDL SQLite
DATABASE_URL = "sqlite:///D:\\Code\\BachKhoa\\PBL 5\\PBL05_smart_home_with_voice_print_and_antifraud_ai\\BackEnd\\db.sqlite3"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Truy vấn dữ liệu
members = session.query(Member).all()
appliances = session.query(Appliance).all()
permissions = session.query(Permission).all()

print("Members:")
for member in members:
    print(member)

print("\nAppliances:")
for appliance in appliances:
    print(appliance)

print("\nPermissions:")
for permission in permissions:
    print(permission)
