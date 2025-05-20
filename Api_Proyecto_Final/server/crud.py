from sqlalchemy.orm import Session
import models
from models import DevicesInfo, DevicesInfoDB, DevicesRecords, DevicesRecordsDB, TomaDecisiones, TomaDecisionesDB, Luces, LucesDB, ControladorVoltaje, ControladorVoltajeDB
from datetime import datetime


# Operaciones CRUD para Test
# CRUD operations for Test

# Obtener todos los tests
# Get all tests
def get_test(db: Session):
    return db.query(models.Test).all()

# Crear un nuevo test
# Create a new test
def create_test(db: Session, title: str):
    new_test = models.Test(name=title)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test

# Obtener un test por ID
# Get a test by ID
def get_test_by_id(db: Session, id: int):
    return db.query(models.Test).filter(models.Test.id == id).first()

# Eliminar un test
# Delete a test
def delete_test(db: Session, id: int):
    task = db.query(models.Test).filter(models.Test.id == id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False


# Operaciones CRUD para DevicesInfo (Información de Dispositivos)
# CRUD operations for DevicesInfo

# Obtener información de todos los dispositivos
# Get all devices info
def get_all_devices_info(db: Session, id_device:int):
    return db.query(models.DevicesInfoDB).all()

# Obtener información de un dispositivo por ID
# Get device info by ID
def get_devices_info_by_id(db: Session, id_device:int):
    return db.query(models.DevicesInfoDB).filter(models.DevicesInfoDB.id_device == id_device).all()

# Eliminar información de un dispositivo
# Delete device info
def delete_device_info(db: Session, id_device:int):
    device = db.query(models.DevicesInfoDB).filter(models.DevicesInfoDB.id_device == id_device).first()
    if device:
        db.delete(device)
        db.commit()
        return True
    return False

# Crear información de un nuevo dispositivo
# Create new device info
def create_device_info(db: Session, device_info: DevicesInfo):
    db_device_info = DevicesInfoDB(
        id_device=device_info.id_device,
        id_type=device_info.id_type,
        id_signal_type=device_info.id_signal_type,
        nombre=device_info.nombre,
        vendor=device_info.vendor,
    )
    db.add(db_device_info)
    db.commit()
    db.refresh(db_device_info)
    return db_device_info

# Actualizar información de un dispositivo
# Update device info
def update_device_info(db: Session, id_device: int, device_info: DevicesInfo):
    db_device_info = db.query(DevicesInfoDB).filter(DevicesInfoDB.id_device == id_device).first()
    if db_device_info:
        db_device_info.id_type = device_info.id_type
        db_device_info.id_signal_type = device_info.id_signal_type
        db_device_info.nombre = device_info.nombre
        db_device_info.vendor = device_info.vendor
        db.commit()
        db.refresh(db_device_info)
        return db_device_info
    return None

# Operaciones CRUD para DevicesRecords (Registros de Dispositivos)
# CRUD operations for DevicesRecords

# Obtener todos los registros de dispositivos
# Get all device records
def get_all_devices_records(db: Session):
    return db.query(DevicesRecordsDB).all()

# Obtener un registro de dispositivo por ID
# Get device record by ID
def get_devices_records_by_id(db: Session, id_record: int):
    return db.query(DevicesRecordsDB).filter(DevicesRecordsDB.id_record == id_record).first()

# Obtener registros de dispositivo por ID de dispositivo
# Get device records by device ID
def get_devices_records_by_device_id(db: Session, id_device: int):
    return db.query(DevicesRecordsDB).filter(DevicesRecordsDB.id_device == id_device).all()

# Crear un nuevo registro de dispositivo
# Create a new device record
def create_device_record(db: Session, device_record: DevicesRecords):
    db_device_record = DevicesRecordsDB(
        id_record=device_record.id_record,
        id_device=device_record.id_device,
        current_value=device_record.current_value,
        date_record=device_record.date_record
    )
    db.add(db_device_record)
    db.commit()
    db.refresh(db_device_record)
    return db_device_record

# Actualizar un registro de dispositivo
# Update a device record
def update_device_record(db: Session, id_record: int, device_record: DevicesRecords):
    db_device_record = db.query(DevicesRecordsDB).filter(DevicesRecordsDB.id_record == id_record).first()
    if db_device_record:
        db_device_record.id_device = device_record.id_device
        db_device_record.current_value = device_record.current_value
        db_device_record.date_record = device_record.date_record
        db.commit()
        db.refresh(db_device_record)
        return db_device_record
    return None

# Eliminar un registro de dispositivo
# Delete a device record
def delete_device_record(db: Session, id_record: int):
    device_record = db.query(DevicesRecordsDB).filter(DevicesRecordsDB.id_record == id_record).first()
    if device_record:
        db.delete(device_record)
        db.commit()
        return True
    return False

# Operaciones CRUD para TomaDecisiones (Toma de Decisiones)
# CRUD operations for TomaDecisiones

# Obtener todas las decisiones
# Get all decisions
def get_all_toma_decisiones(db: Session):
    return db.query(TomaDecisionesDB).all()

# Obtener una decisión por ID
# Get a decision by ID
def get_toma_decisiones_by_id(db: Session, id_decision: int):
    return db.query(TomaDecisionesDB).filter(TomaDecisionesDB.id_decision == id_decision).first()

# Crear una nueva decisión
# Create a new decision
def create_toma_decisiones(db: Session, toma_decisiones: TomaDecisiones):
    db_toma_decisiones = TomaDecisionesDB(
        id_decision=toma_decisiones.id_decision,
        velocidad=toma_decisiones.velocidad,
        decision=toma_decisiones.decision,
        date_record=toma_decisiones.date_record
    )
    db.add(db_toma_decisiones)
    db.commit()
    db.refresh(db_toma_decisiones)
    return db_toma_decisiones

# Actualizar una decisión
# Update a decision
def update_toma_decisiones(db: Session, id_decision: int, toma_decisiones: TomaDecisiones):
    db_toma_decisiones = db.query(TomaDecisionesDB).filter(TomaDecisionesDB.id_decision == id_decision).first()
    if db_toma_decisiones:
        db_toma_decisiones.velocidad = toma_decisiones.velocidad
        db_toma_decisiones.decision = toma_decisiones.decision
        db_toma_decisiones.date_record = toma_decisiones.date_record
        db.commit()
        db.refresh(db_toma_decisiones)
        return db_toma_decisiones
    return None

# Eliminar una decisión
# Delete a decision
def delete_toma_decisiones(db: Session, id_decision: int):
    toma_decisiones = db.query(TomaDecisionesDB).filter(TomaDecisionesDB.id_decision == id_decision).first()
    if toma_decisiones:
        db.delete(toma_decisiones)
        db.commit()
        return True
    return False

# Operaciones CRUD para Luces
# CRUD operations for Luces

# Obtener todas las luces
# Get all lights
def get_all_luces(db: Session):
    return db.query(LucesDB).all()

# Obtener una luz por ID
# Get a light by ID
def get_luces_by_id(db: Session, id_device: int):
    return db.query(LucesDB).filter(LucesDB.id_device == id_device).first()

# Crear una nueva luz
# Create a new light
def create_luces(db: Session, luces: Luces):
    db_luces = LucesDB(
        id_device=luces.id_device,
        lumens=luces.lumens,
        nombre=luces.nombre,
        vendor=luces.vendor
    )
    db.add(db_luces)
    db.commit()
    db.refresh(db_luces)
    return db_luces

# Actualizar una luz
# Update a light
def update_luces(db: Session, id_device: int, luces: Luces):
    db_luces = db.query(LucesDB).filter(LucesDB.id_device == id_device).first()
    if db_luces:
        db_luces.lumens = luces.lumens
        db_luces.nombre = luces.nombre
        db_luces.vendor = luces.vendor
        db.commit()
        db.refresh(db_luces)
        return db_luces
    return None

# Eliminar una luz
# Delete a light
def delete_luces(db: Session, id_device: int):
    luces = db.query(LucesDB).filter(LucesDB.id_device == id_device).first()
    if luces:
        db.delete(luces)
        db.commit()
        return True
    return False

# Operaciones CRUD para ControladorVoltaje
# CRUD operations for ControladorVoltaje

# Obtener todos los controladores de voltaje
# Get all voltage controllers
def get_all_controlador_voltaje(db: Session):
    return db.query(ControladorVoltajeDB).all()

# Obtener un controlador de voltaje por ID
# Get a voltage controller by ID
def get_controlador_voltaje_by_id(db: Session, id_device: int):
    return db.query(ControladorVoltajeDB).filter(ControladorVoltajeDB.id_device == id_device).first()

# Crear un nuevo controlador de voltaje
# Create a new voltage controller
def create_controlador_voltaje(db: Session, controlador_voltaje: ControladorVoltaje):
    db_controlador_voltaje = ControladorVoltajeDB(
        id_device=controlador_voltaje.id_device,
        encendido=1 if controlador_voltaje.encendido else 0,  # Convertir booleano a entero / Convert boolean to integer
        voltaje=controlador_voltaje.voltaje,
        nombre=controlador_voltaje.nombre,
        vendor=controlador_voltaje.vendor
    )
    db.add(db_controlador_voltaje)
    db.commit()
    db.refresh(db_controlador_voltaje)
    return db_controlador_voltaje

# Actualizar un controlador de voltaje
# Update a voltage controller
def update_controlador_voltaje(db: Session, id_device: int, controlador_voltaje: ControladorVoltaje):
    db_controlador_voltaje = db.query(ControladorVoltajeDB).filter(ControladorVoltajeDB.id_device == id_device).first()
    if db_controlador_voltaje:
        db_controlador_voltaje.encendido = 1 if controlador_voltaje.encendido else 0  # Convertir booleano a entero / Convert boolean to integer
        db_controlador_voltaje.voltaje = controlador_voltaje.voltaje
        db_controlador_voltaje.nombre = controlador_voltaje.nombre
        db_controlador_voltaje.vendor = controlador_voltaje.vendor
        db.commit()
        db.refresh(db_controlador_voltaje)
        return db_controlador_voltaje
    return None

# Eliminar un controlador de voltaje
# Delete a voltage controller
def delete_controlador_voltaje(db: Session, id_device: int):
    controlador_voltaje = db.query(ControladorVoltajeDB).filter(ControladorVoltajeDB.id_device == id_device).first()
    if controlador_voltaje:
        db.delete(controlador_voltaje)
        db.commit()
        return True
    return False
