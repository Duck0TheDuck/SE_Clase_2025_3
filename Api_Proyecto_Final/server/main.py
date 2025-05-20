import os
from datetime import datetime

import dotenv
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models, crud
from database import SessionLocal, engine
from typing import List, Optional
from models import (
    DevicesInfo, DevicesRecords, TomaDecisiones, Luces, ControladorVoltaje,
    DevicesInfoDB, DevicesRecordsDB, TomaDecisionesDB, LucesDB, ControladorVoltajeDB,
    TestModel, DevicesInfoResponse, DevicesRecordsResponse, TomaDecisionesResponse,
    LucesResponse, ControladorVoltajeResponse
)

# Crear tablas de base de datos
# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Dispositivos IoT", 
              description="API para gestionar dispositivos IoT y sus registros",
              version="1.0.0")

# Dependencia para la sesión de base de datos
# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Dispositivos IoT"}

# Operaciones CRUD de Test
# Test CRUD operations
@app.get("/tests/", response_model=list[TestModel], tags=["Test"])
def read_tests(db: Session = Depends(get_db)):
    tests = crud.get_test(db)
    return tests

@app.get("/tests/{test_id}", response_model=TestModel, tags=["Test"])
def read_test(test_id: int, db: Session = Depends(get_db)):
    test = crud.get_test_by_id(db, test_id)
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@app.post("/tests/", response_model=TestModel, status_code=status.HTTP_201_CREATED, tags=["Test"])
def create_test(title: str, db: Session = Depends(get_db)):
    return crud.create_test(db, title)

@app.delete("/tests/{test_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Test"])
def delete_test(test_id: int, db: Session = Depends(get_db)):
    success = crud.delete_test(db, test_id)
    if not success:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": "Test deleted successfully"}

# Actualizar los endpoints de DevicesInfo (Información de Dispositivos)
# Update the DevicesInfo endpoints
@app.get("/devices/info/", response_model=list[DevicesInfoResponse], tags=["DevicesInfo"])
def read_devices_info(db: Session = Depends(get_db)):
    devices_info = crud.get_all_devices_info(db, 0)
    return devices_info

@app.get("/devices/info/{id_device}", response_model=list[DevicesInfoResponse], tags=["DevicesInfo"])
def read_device_info(id_device: int, db: Session = Depends(get_db)):
    device_info = crud.get_devices_info_by_id(db, id_device)
    if not device_info:
        raise HTTPException(status_code=404, detail="Device info not found")
    return device_info

@app.post("/devices/info/", response_model=DevicesInfoResponse, status_code=status.HTTP_201_CREATED, tags=["DevicesInfo"])
def create_device_info(device_info: DevicesInfo, db: Session = Depends(get_db)):
    return crud.create_device_info(db, device_info)

@app.put("/devices/info/{id_device}", response_model=DevicesInfoResponse, tags=["DevicesInfo"])
def update_device_info(id_device: int, device_info: DevicesInfo, db: Session = Depends(get_db)):
    updated_device = crud.update_device_info(db, id_device, device_info)
    if updated_device is None:
        raise HTTPException(status_code=404, detail="Device info not found")
    return updated_device

@app.delete("/devices/info/{id_device}", status_code=status.HTTP_204_NO_CONTENT, tags=["DevicesInfo"])
def delete_device_info(id_device: int, db: Session = Depends(get_db)):
    success = crud.delete_device_info(db, id_device)
    if not success:
        raise HTTPException(status_code=404, detail="Device info not found")
    return {"message": "Device info deleted successfully"}

# Operaciones CRUD de DevicesRecords (Registros de Dispositivos)
# DevicesRecords CRUD operations
@app.get("/devices/records/", response_model=list[DevicesRecordsResponse], tags=["DevicesRecords"])
def read_devices_records(db: Session = Depends(get_db)):
    devices_records = crud.get_all_devices_records(db)
    return devices_records

@app.get("/devices/records/{id_record}", response_model=DevicesRecordsResponse, tags=["DevicesRecords"])
def read_device_record(id_record: int, db: Session = Depends(get_db)):
    device_record = crud.get_devices_records_by_id(db, id_record)
    if device_record is None:
        raise HTTPException(status_code=404, detail="Device record not found")
    return device_record

# Actualizar endpoint de DevicesRecords que todavía usa DevicesRecordsDB
# Update DevicesRecords endpoint that still uses DevicesRecordsDB
@app.get("/devices/records/device/{id_device}", response_model=list[DevicesRecordsResponse], tags=["DevicesRecords"])
def read_device_records_by_device(id_device: int, db: Session = Depends(get_db)):
    device_records = crud.get_devices_records_by_device_id(db, id_device)
    if not device_records:
        raise HTTPException(status_code=404, detail="No se encontraron registros para este dispositivo")
    return device_records

@app.post("/devices/records/", response_model=DevicesRecordsResponse, status_code=status.HTTP_201_CREATED, tags=["DevicesRecords"])
def create_device_record(device_record: DevicesRecords, db: Session = Depends(get_db)):
    return crud.create_device_record(db, device_record)

@app.put("/devices/records/{id_record}", response_model=DevicesRecordsResponse, tags=["DevicesRecords"])
def update_device_record(id_record: int, device_record: DevicesRecords, db: Session = Depends(get_db)):
    updated_record = crud.update_device_record(db, id_record, device_record)
    if updated_record is None:
        raise HTTPException(status_code=404, detail="Device record not found")
    return updated_record

@app.delete("/devices/records/{id_record}", status_code=status.HTTP_204_NO_CONTENT, tags=["DevicesRecords"])
def delete_device_record(id_record: int, db: Session = Depends(get_db)):
    success = crud.delete_device_record(db, id_record)
    if not success:
        raise HTTPException(status_code=404, detail="Device record not found")
    return {"message": "Device record deleted successfully"}

# Actualizar endpoints de TomaDecisiones (Toma de Decisiones)
# Update TomaDecisiones endpoints
@app.get("/decisiones/", response_model=list[TomaDecisionesResponse], tags=["TomaDecisiones"])
def read_toma_decisiones(db: Session = Depends(get_db)):
    decisiones = crud.get_all_toma_decisiones(db)
    return decisiones

@app.get("/decisiones/{id_decision}", response_model=TomaDecisionesResponse, tags=["TomaDecisiones"])
def read_toma_decision(id_decision: int, db: Session = Depends(get_db)):
    decision = crud.get_toma_decisiones_by_id(db, id_decision)
    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

@app.post("/decisiones/", response_model=TomaDecisionesResponse, status_code=status.HTTP_201_CREATED, tags=["TomaDecisiones"])
def create_toma_decision(toma_decision: TomaDecisiones, db: Session = Depends(get_db)):
    return crud.create_toma_decisiones(db, toma_decision)

@app.put("/decisiones/{id_decision}", response_model=TomaDecisionesResponse, tags=["TomaDecisiones"])
def update_toma_decision(id_decision: int, toma_decision: TomaDecisiones, db: Session = Depends(get_db)):
    updated_decision = crud.update_toma_decisiones(db, id_decision, toma_decision)
    if updated_decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return updated_decision

@app.delete("/decisiones/{id_decision}", status_code=status.HTTP_204_NO_CONTENT, tags=["TomaDecisiones"])
def delete_toma_decision(id_decision: int, db: Session = Depends(get_db)):
    success = crud.delete_toma_decisiones(db, id_decision)
    if not success:
        raise HTTPException(status_code=404, detail="Decision not found")
    return {"message": "Decision deleted successfully"}

# Actualizar endpoints de Luces
# Update Luces endpoints
@app.get("/luces/", response_model=list[LucesResponse], tags=["Luces"])
def read_luces(db: Session = Depends(get_db)):
    luces = crud.get_all_luces(db)
    return luces

@app.get("/luces/{id_device}", response_model=LucesResponse, tags=["Luces"])
def read_luz(id_device: int, db: Session = Depends(get_db)):
    luz = crud.get_luces_by_id(db, id_device)
    if luz is None:
        raise HTTPException(status_code=404, detail="Luz not found")
    return luz

@app.post("/luces/", response_model=LucesResponse, status_code=status.HTTP_201_CREATED, tags=["Luces"])
def create_luz(luz: Luces, db: Session = Depends(get_db)):
    return crud.create_luces(db, luz)

@app.put("/luces/{id_device}", response_model=LucesResponse, tags=["Luces"])
def update_luz(id_device: int, luz: Luces, db: Session = Depends(get_db)):
    updated_luz = crud.update_luces(db, id_device, luz)
    if updated_luz is None:
        raise HTTPException(status_code=404, detail="Luz not found")
    return updated_luz

@app.delete("/luces/{id_device}", status_code=status.HTTP_204_NO_CONTENT, tags=["Luces"])
def delete_luz(id_device: int, db: Session = Depends(get_db)):
    success = crud.delete_luces(db, id_device)
    if not success:
        raise HTTPException(status_code=404, detail="Luz not found")
    return {"message": "Luz deleted successfully"}

# Actualizar endpoints de ControladorVoltaje
# Update ControladorVoltaje endpoints
@app.get("/controladores/", response_model=list[ControladorVoltajeResponse], tags=["ControladorVoltaje"])
def read_controladores(db: Session = Depends(get_db)):
    controladores = crud.get_all_controlador_voltaje(db)
    return controladores

@app.get("/controladores/{id_device}", response_model=ControladorVoltajeResponse, tags=["ControladorVoltaje"])
def read_controlador(id_device: int, db: Session = Depends(get_db)):
    controlador = crud.get_controlador_voltaje_by_id(db, id_device)
    if controlador is None:
        raise HTTPException(status_code=404, detail="Controlador not found")
    return controlador

@app.post("/controladores/", response_model=ControladorVoltajeResponse, status_code=status.HTTP_201_CREATED, tags=["ControladorVoltaje"])
def create_controlador(controlador: ControladorVoltaje, db: Session = Depends(get_db)):
    return crud.create_controlador_voltaje(db, controlador)

@app.put("/controladores/{id_device}", response_model=ControladorVoltajeResponse, tags=["ControladorVoltaje"])
def update_controlador(id_device: int, controlador: ControladorVoltaje, db: Session = Depends(get_db)):
    updated_controlador = crud.update_controlador_voltaje(db, id_device, controlador)
    if updated_controlador is None:
        raise HTTPException(status_code=404, detail="Controlador not found")
    return updated_controlador

@app.delete("/controladores/{id_device}", status_code=status.HTTP_204_NO_CONTENT, tags=["ControladorVoltaje"])
def delete_controlador(id_device: int, db: Session = Depends(get_db)):
    success = crud.delete_controlador_voltaje(db, id_device)
    if not success:
        raise HTTPException(status_code=404, detail="Controlador not found")
    return {"message": "Controlador deleted successfully"}
