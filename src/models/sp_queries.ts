//TODO SP_FUNCTIONS DE CRUD
import {Client} from 'pg';
import {get_connection} from "./conexion_db.js";

const client = get_connection()

async function sp_insert_decision(velocidad_param_numeric:number,distancia_param_numeric:number,decision_param_numeric:number) {
    try {
        const res = await client.query('SELECT sp_insert_decision($1,$2,$3) AS result', [velocidad_param_numeric,distancia_param_numeric, decision_param_numeric]);
    } catch (error) {
        console.log(error);
    } finally {
        await client.end();
    }
}