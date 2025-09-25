from sqlalchemy import Column, Integer, String, LargeBinary
from app.database.database import Base

class Face(Base):
    __tablename__ = "faces"  # Fixed: was **tablename** should be __tablename__
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    embedding = Column(LargeBinary)  # Store face embedding as binary