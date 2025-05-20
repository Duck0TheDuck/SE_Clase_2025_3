const {getConnection} = require('./conexion')
const sql = require('mssql')

const Sp_SelectALL_records  = async function(){    
    const conexion = await getConnection()
    const result = await conexion
    .request().execute('SP_SelectALL_records')
    //console.log(result.recordset)
    return result.recordset
}

const SP_SelecLastRecordByID = async function(ID){    
    const conexion = await getConnection()
    const result = await conexion
    .request()                      
         .input("id_device", sql.Int, ID )        
         .execute('SP_SelecLastRecordByID')
    console.log(result.recordset)
    return result.recordset[0]
}

const Sp_SelecLastDecision = async function(){    
    const conexion = await getConnection()
    const result = await conexion
    .request().execute('Sp_SelecLastDecision')
    return result.recordset[0]
}

const SP_Insert_DevicesRecords = async function(id_device, current_value){

    console.log("id_device: ", id_device, " current_value:", current_value)

    const conexion = await getConnection()
    const result = await conexion
    .request()                
         .input("id_device", sql.Int, id_device )        
         .input("current_value", sql.Int, current_value  )        
         .execute('SP_Insert_DevicesRecords')
    //console.log(result)
    return "{\"Resultado\": \"Insercion Correcta\"}"
}

const Sp_Insert_Decision = async function(velocidad, distancia, decision){

    console.log("velocidad: ", velocidad, " distancia:", distancia, " decision:",  decision)

    const conexion = await getConnection()
    const result = await conexion
    .request()                         
         .input("velocidad", sql.Int, velocidad  )        
         .input("distancia", sql.Int, distancia )        
         .input("decision", sql.Int, decision )        
         .execute('Sp_Insert_Decision')
    //console.log(result)
    return "{\"Resultado\": \"Insercion Correcta\"}"
}

///////////////////////////////////////////////////////////////////////////////////////////////////
//EXPORTA LAS FUNCIONES PARA HACER POSIBLE SU POSTERIOR IMPORTANCION Y USO EN OTROS MODULOS
module.exports = {
    Sp_SelectALL_records, 
    SP_SelecLastRecordByID,
    Sp_SelecLastDecision,  

    SP_Insert_DevicesRecords,
    Sp_Insert_Decision,  

}
