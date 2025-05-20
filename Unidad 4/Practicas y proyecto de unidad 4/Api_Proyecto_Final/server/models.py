from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.sql.sqltypes import Float as SQLAlchemyFloat, Date,Numeric
from pydantic import BaseModel
from database import  Base
from datetime import datetime


# Clase de prueba para testing
# Test class for testing
class Test(Base):
    __tablename__ = "Testing"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    value = Column(String)


# Modelo Pydantic para Test
# Pydantic model for Test
class TestModel(BaseModel):
    id: int
    name: str
    value: str


# Modelo SQLAlchemy para información de dispositivos
# SQLAlchemy model for device information
class DevicesInfoDB(Base):
    __tablename__ = "DevicesInfo"
    id_device = Column(Integer, primary_key=True, index=True,nullable=False,unique=True,autoincrement=True)
    id_type = Column(Numeric, primary_key=False, index=False,nullable=False,unique=True,autoincrement=False)
    id_signal_type = Column(Numeric, primary_key=False, index=False,nullable=False,unique=True,autoincrement=False)
    nombre = Column(String, unique=False, index=True,nullable=False)
    vendor = Column(String, unique=False, index=True,nullable=False)


# Modelo SQLAlchemy para registros de dispositivos
# SQLAlchemy model for device records
class DevicesRecordsDB(Base):
    __tablename__ = "DevicesRecords"
    id_record = Column(Integer, primary_key=True, index=True,nullable=False,unique=True,autoincrement=True)
    id_device = Column(Numeric, primary_key=False, index=False,nullable=False,unique=False,autoincrement=False)
    current_value = Column(Numeric,index=False,unique=False,nullable=False)
    date_record = Column(Date,index=False,unique=False,nullable=False)

# Modelo SQLAlchemy para toma de decisiones
# SQLAlchemy model for decision making
class TomaDecisionesDB(Base):
    __tablename__ = "TomaDecisiones"
    id_decision = Column(Integer, primary_key=True, index=True,nullable=False,unique=True,autoincrement=True)
    velocidad = Column(Numeric,index=False,unique=False,nullable=False)
    decision = Column(Numeric,index=False,unique=False,nullable=False)
    date_record = Column(Date,index=False,unique=False,nullable=False)


# Modelo Pydantic para solicitudes de información de dispositivos
# Pydantic model for device information requests
class DevicesInfo(BaseModel):

    id_device:int
    id_type:int
    id_signal_type:int
    nombre:str
    vendor:str

# Modelo Pydantic para respuestas de información de dispositivos
# Pydantic model for device information responses
class DevicesInfoResponse(BaseModel):
    id_device: int
    id_type: float  # Changed to float since DB uses Numeric
    id_signal_type: float  # Changed to float since DB uses Numeric
    nombre: str
    vendor: str

    class Config:
        from_attributes = True


# Modelo Pydantic para registros de dispositivos
# Pydantic model for device records
class DevicesRecords(BaseModel):

    id_record:int
    id_device:int
    current_value:float
    date_record:datetime


# Modelo Pydantic para toma de decisiones
# Pydantic model for decision making
class TomaDecisiones(BaseModel):

    id_decision:int
    velocidad:float
    decision:float
    date_record:datetime

# Modelo Pydantic para luces
# Pydantic model for lights
class Luces(BaseModel):
    lumens:float
    id_device:int
    nombre:str
    vendor:str


# Modelo Pydantic para controlador de voltaje
# Pydantic model for voltage controller
class ControladorVoltaje(BaseModel):
    encendido:bool
    voltaje:float
    id_device:int
    nombre:str
    vendor:str

# Modelo SQLAlchemy para luces
# SQLAlchemy model for lights
class LucesDB(Base):
    __tablename__ = "Luces"
    id_device = Column(Integer, primary_key=True, index=True, nullable=False, unique=True, autoincrement=True)
    lumens = Column(Numeric, index=False, unique=False, nullable=False)
    nombre = Column(String, unique=False, index=True, nullable=False)
    vendor = Column(String, unique=False, index=True, nullable=False)

# Modelo SQLAlchemy para controlador de voltaje
# SQLAlchemy model for voltage controller
class ControladorVoltajeDB(Base):
    __tablename__ = "ControladorVoltaje"
    id_device = Column(Integer, primary_key=True, index=True, nullable=False, unique=True, autoincrement=True)
    encendido = Column(Integer, index=False, unique=False, nullable=False)  # Using Integer for boolean
    voltaje = Column(Numeric, index=False, unique=False, nullable=False)
    nombre = Column(String, unique=False, index=True, nullable=False)
    vendor = Column(String, unique=False, index=True, nullable=False)

# Añadir estos modelos de respuesta Pydantic después de tus modelos existentes
# Add these Pydantic response models after your existing models
class DevicesRecordsResponse(BaseModel):
    id_record: int
    id_device: float
    current_value: float
    date_record: datetime

    class Config:
        from_attributes = True

# Modelo de respuesta para toma de decisiones
# Response model for decision making
class TomaDecisionesResponse(BaseModel):
    id_decision: int
    velocidad: float
    decision: float
    date_record: datetime

    class Config:
        from_attributes = True

# Modelo de respuesta para luces
# Response model for lights
class LucesResponse(BaseModel):
    id_device: int
    lumens: float
    nombre: str
    vendor: str

    class Config:
        from_attributes = True

# Modelo de respuesta para controlador de voltaje
# Response model for voltage controller
class ControladorVoltajeResponse(BaseModel):
    id_device: int
    encendido: bool
    voltaje: float
    nombre: str
    vendor: str

    class Config:
        from_attributes = True
