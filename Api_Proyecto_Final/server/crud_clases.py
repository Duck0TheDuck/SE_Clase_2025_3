from sqlalchemy.orm import Session
import models
from models import DevicesRecords,DevicesRecordsDB,DevicesInfo,DevicesInfoDB

def create_device_info(db:Session, device_info: DevicesInfo):
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

def read_all_device_info(db:Session):
    return db.query(DevicesInfo).all()

def read_by_id(db:Session, id_device:int):
    return db.query(DevicesInfo).filter(DevicesInfoDB.id_device == id_device).first()

def delete_device_info(db:Session, id_device:int):
    device = db.query(DevicesInfoDB).filter(DevicesInfoDB.id_device == id_device).all()
    if device:
        db.delete(device)
        db.commit()
        return True
    return False


