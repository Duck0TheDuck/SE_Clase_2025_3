# API de Dispositivos IoT

Esta es una aplicación FastAPI para gestionar dispositivos IoT y sus registros. La API proporciona operaciones CRUD para varios tipos de dispositivos y sus datos.

## Configuración e Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala las dependencias requeridas:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
   ```
3. Configura tu conexión a la base de datos en el archivo `.env`:
   ```
   DATABASE_URL=sqlite:///./iot_devices.db
   ```

## Ejecutando la API

Para ejecutar la API, utiliza el siguiente comando desde el directorio `server`:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en `http://localhost:8000`.

## Documentación de la API

Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación de la API generada automáticamente en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints de la API

La API proporciona los siguientes endpoints:

### Test
- `GET /tests/` - Obtener todos los tests
- `GET /tests/{test_id}` - Obtener un test por ID
- `POST /tests/?title={title}` - Crear un nuevo test
- `DELETE /tests/{test_id}` - Eliminar un test

### DevicesInfo (Información de Dispositivos)
- `GET /devices/info/` - Obtener información de todos los dispositivos
- `GET /devices/info/{id_device}` - Obtener información de un dispositivo por ID
- `POST /devices/info/` - Crear información de un nuevo dispositivo
- `PUT /devices/info/{id_device}` - Actualizar información de un dispositivo
- `DELETE /devices/info/{id_device}` - Eliminar información de un dispositivo

### DevicesRecords (Registros de Dispositivos)
- `GET /devices/records/` - Obtener todos los registros de dispositivos
- `GET /devices/records/{id_record}` - Obtener un registro de dispositivo por ID
- `GET /devices/records/device/{id_device}` - Obtener registros de dispositivo por ID de dispositivo
- `POST /devices/records/` - Crear un nuevo registro de dispositivo
- `PUT /devices/records/{id_record}` - Actualizar un registro de dispositivo
- `DELETE /devices/records/{id_record}` - Eliminar un registro de dispositivo

### TomaDecisiones (Toma de Decisiones)
- `GET /decisiones/` - Obtener todas las decisiones
- `GET /decisiones/{id_decision}` - Obtener una decisión por ID
- `POST /decisiones/` - Crear una nueva decisión
- `PUT /decisiones/{id_decision}` - Actualizar una decisión
- `DELETE /decisiones/{id_decision}` - Eliminar una decisión

### Luces
- `GET /luces/` - Obtener todas las luces
- `GET /luces/{id_device}` - Obtener una luz por ID
- `POST /luces/` - Crear una nueva luz
- `PUT /luces/{id_device}` - Actualizar una luz
- `DELETE /luces/{id_device}` - Eliminar una luz

### ControladorVoltaje
- `GET /controladores/` - Obtener todos los controladores de voltaje
- `GET /controladores/{id_device}` - Obtener un controlador de voltaje por ID
- `POST /controladores/` - Crear un nuevo controlador de voltaje
- `PUT /controladores/{id_device}` - Actualizar un controlador de voltaje
- `DELETE /controladores/{id_device}` - Eliminar un controlador de voltaje

## Ejemplos de Solicitudes a la API

El archivo `api_requests_examples.http` contiene ejemplos de solicitudes HTTP para todas las operaciones CRUD. Puedes usar estos ejemplos con REST Client en VS Code o herramientas similares.

Para usar los ejemplos:
1. Instala la extensión REST Client en VS Code
2. Abre el archivo `api_requests_examples.http`
3. Haz clic en el enlace "Send Request" encima de cada solicitud para ejecutarla

Alternativamente, puedes usar herramientas como Postman o curl para hacer solicitudes a la API.

## Modelos

La API utiliza los siguientes modelos:

### DevicesInfo (Información de Dispositivos)
```json
{
  "id_device": 1,
  "id_type": 1,
  "id_signal_type": 1,
  "nombre": "Sensor de Temperatura",
  "vendor": "Acme Inc."
}
```

### DevicesRecords (Registros de Dispositivos)
```json
{
  "id_record": 1,
  "id_device": 1,
  "current_value": 25.5,
  "date_record": "2023-06-01T12:00:00"
}
```

### TomaDecisiones
```json
{
  "id_decision": 1,
  "velocidad": 50.5,
  "decision": 1,
  "date_record": "2023-06-01T12:00:00"
}
```

### Luces
```json
{
  "id_device": 1,
  "lumens": 800,
  "nombre": "Luz de Sala de Estar",
  "vendor": "Philips"
}
```

### ControladorVoltaje
```json
{
  "id_device": 1,
  "encendido": true,
  "voltaje": 220.0,
  "nombre": "Controlador de Energía Principal",
  "vendor": "Siemens"
}
```