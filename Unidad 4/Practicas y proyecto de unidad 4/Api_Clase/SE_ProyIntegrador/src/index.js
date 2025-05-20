const express = require('express') // importacion de modulo para crear la api
const v1 = require('./v1/routes/Routes')

const app = express();
const PORT = process.env.PORT || 3000;
app.use(express.json()) //json parser --//habilita a la api para trabajar con json

//vincula las rutas ("NOMBRE" QUE SE USARA PARA LLAMAR A LAS RUTAS)
//app.use("/api/v1-sensors/sensors", v1Sensors)

// http://localhost:3000    127.0.0.1
// http://ip local / publica / homologada / privada
// http://DNS
// /api/v1-actuators/actuators

app.use("/api/v1", v1)

///////////////Informacion que se despliega al acceder a http://localhost:3000/ ...
app.get("/",(req,res)=>{
    res.send(`<h1>API RESTful en NodeJS para Servicios Embebidos</h1>`)
})
//////////////////

//inicia la api y ejecuta una funcion callback que retroalimenta el estado en la consola/terminal
app.listen(PORT, function(){ //()=>{  //funcion flecha
    console.log(`Servidor escuchando en el Puerto: ${PORT}`);
})