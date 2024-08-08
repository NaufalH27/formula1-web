const mysql = require('mysql2/promise');
require('dotenv').config();

let instance = null;

class Database {
    constructor() {
        if (!instance) {
            instance = this;
            this.init();
        }
        return instance;
    }

    async init() {
        this.connection = await mysql.createConnection({
            host: process.env.DB_HOST,
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
            database: process.env.DB
        });
        console.log('Database connection established');
    }

    async query(sql, params) {
        try {
            const [rows, fields] = await this.connection.execute(sql, params);
            return rows;
        } catch (error) {
            console.error('Database query error:', error);
            throw error;
        }
    }

    async close() {
        await this.connection.end();
        console.log('Database connection closed');
    }
}

const dbInstance = new Database();

module.exports = dbInstance;