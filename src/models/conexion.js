const sql = require('mssql')

const config = {
    user:'sa',
    password:'Prueba123',
    server:'localhost',
    database:'BD_UNIDAD_4_SE_2025_1',
    options: {
        encrypt: true, // for azure
        trustServerCertificate: true // change to true for local dev / self-signed certs
      }
}

const getConnection = async function (){
    try{
        const conexion = await sql.connect(config) //conexion es el objeto que representa la conexion logica con la base de datos
        return conexion
    }
    catch(error){
        console.log(error)
    }    
}

module.exports = {
    getConnection
}
