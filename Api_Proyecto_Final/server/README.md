# IoT Devices API

This is a FastAPI application for managing IoT devices and their records. The API provides CRUD operations for various types of devices and their data.

## Setup and Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
   ```
3. Configure your database connection in the `.env` file:
   ```
   DATABASE_URL=sqlite:///./iot_devices.db
   ```

## Running the API

To run the API, use the following command from the `server` directory:

```bash
uvicorn main:app --reload
```

This will start the server at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

The API provides the following endpoints:

### Test
- `GET /tests/` - Get all tests
- `GET /tests/{test_id}` - Get a test by ID
- `POST /tests/?title={title}` - Create a new test
- `DELETE /tests/{test_id}` - Delete a test

### DevicesInfo
- `GET /devices/info/` - Get all devices info
- `GET /devices/info/{id_device}` - Get device info by ID
- `POST /devices/info/` - Create a new device info
- `PUT /devices/info/{id_device}` - Update a device info
- `DELETE /devices/info/{id_device}` - Delete a device info

### DevicesRecords
- `GET /devices/records/` - Get all device records
- `GET /devices/records/{id_record}` - Get a device record by ID
- `GET /devices/records/device/{id_device}` - Get device records by device ID
- `POST /devices/records/` - Create a new device record
- `PUT /devices/records/{id_record}` - Update a device record
- `DELETE /devices/records/{id_record}` - Delete a device record

### TomaDecisiones
- `GET /decisiones/` - Get all decisions
- `GET /decisiones/{id_decision}` - Get a decision by ID
- `POST /decisiones/` - Create a new decision
- `PUT /decisiones/{id_decision}` - Update a decision
- `DELETE /decisiones/{id_decision}` - Delete a decision

### Luces
- `GET /luces/` - Get all lights
- `GET /luces/{id_device}` - Get a light by ID
- `POST /luces/` - Create a new light
- `PUT /luces/{id_device}` - Update a light
- `DELETE /luces/{id_device}` - Delete a light

### ControladorVoltaje
- `GET /controladores/` - Get all voltage controllers
- `GET /controladores/{id_device}` - Get a voltage controller by ID
- `POST /controladores/` - Create a new voltage controller
- `PUT /controladores/{id_device}` - Update a voltage controller
- `DELETE /controladores/{id_device}` - Delete a voltage controller

## Example API Requests

The file `api_requests_examples.http` contains example HTTP requests for all CRUD operations. You can use these with REST Client in VS Code or similar tools.

To use the examples:
1. Install the REST Client extension in VS Code
2. Open the `api_requests_examples.http` file
3. Click on the "Send Request" link above each request to execute it

Alternatively, you can use tools like Postman or curl to make requests to the API.

## Models

The API uses the following models:

### DevicesInfo
```json
{
  "id_device": 1,
  "id_type": 1,
  "id_signal_type": 1,
  "nombre": "Temperature Sensor",
  "vendor": "Acme Inc."
}
```

### DevicesRecords
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
  "nombre": "Living Room Light",
  "vendor": "Philips"
}
```

### ControladorVoltaje
```json
{
  "id_device": 1,
  "encendido": true,
  "voltaje": 220.0,
  "nombre": "Main Power Controller",
  "vendor": "Siemens"
}
```