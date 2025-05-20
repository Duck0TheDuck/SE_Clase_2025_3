import express, { Request, Response } from 'express';
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { Pool } from 'pg';
import dotenv from 'dotenv';
import {pool} from "./models/conexion_db.js";
import {get_connection} from './models/conexion_db.js';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port: number = 3000;

try {
    const conexion = get_connection()
    app.put('/insert_test', async (req: Request, res: Response) => {
    const {velocidad, distancia ,decision} = req.body;
    // @ts-ignore
        const result = await (await conexion).query(
        'SELECT sp_insert_decision($1, $2, $3) AS result',
        [velocidad, distancia, decision]
    );
    })
} catch( err){

}


// Handle application shutdown
process.on('SIGINT', async () => {
    await pool.end();
    process.exit(0);
});