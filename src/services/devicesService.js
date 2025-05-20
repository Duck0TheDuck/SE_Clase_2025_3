const bd = require("../models/DevicesSP")

//SELECT * FROM ... ALL
const getAll_records = async function(){    
    //return " HOLA!!"    
    const resp = await bd.Sp_SelectALL_records()
    console.log("resp from service->", resp)
    return resp
}

//SELECT * FROM .. WHERE ... ID
const getLastDevice_Record = async function(id){
    const resp = await bd.SP_SelecLastRecordByID(id)
    return resp
}

//SELECT * FROM .. INNER JOIN WHERE
const getLastDecision = async function(){
    const resp = await bd.Sp_SelecLastDecision()
    return resp
}

//INSERT
const insertRecord = async function(JsonObj){
    id = JsonObj.Id_device
    current_value  = JsonObj.Current_value
    //console.log("Res: ", JsonObj)
    const resp = await bd.SP_Insert_DevicesRecords(id, current_value)
    return resp
}

//INSERT
const insertDecision = async function(JsonObj){
    Velocidad = JsonObj.Velocidad
    Distancia  = JsonObj.Distancia
    Decision = JsonObj.Decision
    //console.log("Res: ", JsonObj)
    const resp = await bd.Sp_Insert_Decision(Velocidad, Distancia, Decision)
    return resp
}

module.exports = {
    getAll_records,
    getLastDevice_Record,
    getLastDecision,

    insertRecord,
    insertDecision,
    
}

