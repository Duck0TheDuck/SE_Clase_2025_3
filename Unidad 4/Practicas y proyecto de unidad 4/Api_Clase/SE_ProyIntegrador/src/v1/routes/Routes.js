const express = require('express')

const controller = require('../../controllers/devicesController')

//RUTAS
const router = express.Router()

// /api/v1-actuators/actuators
router
   // http://localhost:3000/api/v1/  ->> volley
                                  // --> http
  .get("/", controller.getAll_records) 
  
  // http://localhost:3000/api/v1/optimizar/X
  .get("/optimizar/:idDevice", controller.getLast_Record)

  // http://localhost:3000/api/v1-actuators/decision
  .get("/decision", controller.getLastDecision) 

  // http://localhost:3000/api/v1-actuators/decision/2
  .get("/decision/:idDevice", controller.getLastDecisionEjemplo) 
  
  // http://localhost:3000/api/v1-actuators/decision
  .get("/decision/:idDevice/:idVector", controller.getLastDecisionMultiple) 


  //INSERT NEW RECORD
  // http://localhost:3000/api/v1-actuators/registros/
  .post("/registros", controller.insertRecord) 
  
  //INSERT DECISION
  // http://localhost:3000/api/v1-actuators/decision/
  .post("/decision", controller.insertDecision) 


  
  .delete("/borrar", function(req,res){ 
    res.status(200).send("Dato Borrado")
  })

  .put("/update", function(req,res){ 
    res.status(200).send("Dato Actualizado")
  })

  //EXPORTA EL ROUTER PARA HACER POSIBLE SU POSTERIOR IMPORTANCION Y USO EN OTROS MODULOS
module.exports = router;