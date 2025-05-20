# API RESTful para Sistemas Embebidos

## Descripción
Este proyecto es una API RESTful desarrollada en Node.js para la gestión de datos de dispositivos embebidos. Permite registrar y consultar información de sensores y actuadores, así como almacenar y recuperar decisiones basadas en parámetros como velocidad y distancia.

## Tecnologías Utilizadas
- **Node.js**: Entorno de ejecución para JavaScript
- **Express.js**: Framework para crear APIs RESTful
- **SQL Server**: Base de datos relacional para almacenamiento de datos
- **mssql**: Librería para conectar Node.js con SQL Server

## Requisitos Previos
- Node.js (versión recomendada: 14.x o superior)
- SQL Server instalado y configurado
- Base de datos creada según el script SQL proporcionado

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd SE_ProyIntegrador
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar la base de datos:
   - Ejecutar el script SQL_proyIntegrador.sql en SQL Server para crear la base de datos y las tablas necesarias
   - Verificar y ajustar la configuración de conexión en src/models/conexion.js si es necesario

4. Iniciar la aplicación:
```bash
npm start
```

Para desarrollo con recarga automática:
```bash
npm run prueba
```

## Estructura del Proyecto

```
SE_ProyIntegrador/
├── SQL_proyIntegrador.sql    # Script para crear la base de datos
├── package.json              # Configuración del proyecto y dependencias
├── src/
│   ├── index.js              # Punto de entrada de la aplicación
│   ├── controllers/
│   │   └── devicesController.js  # Controladores para manejar las peticiones
│   ├── models/
│   │   ├── conexion.js       # Configuración de conexión a la base de datos
│   │   └── DevicesSP.js      # Funciones para ejecutar procedimientos almacenados
│   ├── services/
│   │   └── devicesService.js # Servicios para la lógica de negocio
│   └── v1/
│       └── routes/
│           └── Routes.js     # Definición de rutas de la API
```

## Endpoints de la API

### Consultas (GET)

- **GET /api/v1/**
  - Obtiene todos los registros de dispositivos
  - Ejemplo: `http://localhost:3000/api/v1/`

- **GET /api/v1/optimizar/:idDevice**
  - Obtiene el último registro de un dispositivo específico
  - Ejemplo: `http://localhost:3000/api/v1/optimizar/1`

- **GET /api/v1/decision**
  - Obtiene la última decisión tomada
  - Ejemplo: `http://localhost:3000/api/v1/decision`

- **GET /api/v1/decision/:idDevice**
  - Obtiene la última decisión para un dispositivo específico
  - Ejemplo: `http://localhost:3000/api/v1/decision/2`

- **GET /api/v1/decision/:idDevice/:idVector**
  - Obtiene la última decisión con múltiples parámetros
  - Ejemplo: `http://localhost:3000/api/v1/decision/1/2`

### Inserciones (POST)

- **POST /api/v1/registros**
  - Inserta un nuevo registro de dispositivo
  - Cuerpo de la petición:
    ```json
    {
        "Id_device": 1,
        "Current_value": 155
    }
    ```

- **POST /api/v1/decision**
  - Inserta una nueva decisión
  - Cuerpo de la petición:
    ```json
    {
        "Velocidad": 50,
        "Distancia": 25,
        "Decision": 5
    }
    ```

## Base de Datos

La base de datos contiene las siguientes tablas:

1. **devices_info**: Almacena información sobre los dispositivos (sensores o actuadores)
   - id_device: Identificador único del dispositivo
   - id_type: Tipo de dispositivo (sensor o actuador)
   - id_signal_type: Tipo de señal (digital o analógica)
   - name: Nombre del dispositivo
   - vendor: Fabricante del dispositivo

2. **devices_records**: Almacena registros históricos de lecturas de dispositivos
   - id_record: Identificador único del registro
   - id_device: Identificador del dispositivo
   - current_value: Valor actual
   - date_record: Fecha y hora del registro

3. **toma_decisiones**: Almacena datos para la toma de decisiones
   - id_decision: Identificador único de la decisión
   - velocidad: Valor de velocidad
   - distancia: Valor de distancia
   - decision: Valor de la decisión tomada
   - date_record: Fecha y hora del registro

## Procedimientos Almacenados

La base de datos utiliza los siguientes procedimientos almacenados:

1. **SP_Insert_DevicesRecords**: Inserta un nuevo registro de dispositivo
2. **SP_SelectALL_records**: Obtiene todos los registros
3. **SP_SelecLastRecordByID**: Obtiene el último registro de un dispositivo específico
4. **SP_Insert_Decision**: Inserta una nueva decisión
5. **SP_SelecLastDecision**: Obtiene la última decisión tomada