const express = require('express')
const router = express.Router()

// Database
var db = require('../database/db-connector');

// get all paymentTypes
router.get('/', (req, res) => {
    let select_sql = `
        SELECT * FROM PaymentTypes;
    `
    db.pool.query(select_sql, (error, rows, fields) => {
        if (error) {
            console.log(error);
            res.status(400).json({Error: error});
        } else {
            res.status(200).json(rows);
        }
    })
});

// create new paymentType
router.post('/', (req, res) => {
    let data = req.body;
    let create_sql = `
        INSERT INTO PaymentTypes 
            (name, description) 
        VALUES
            ('${data['name']}', '${data['description']}');
    `
    let id_sql = `
        SELECT max(paymentTypeID) as paymentTypeID
        FROM PaymentTypes
        WHERE
            name = '${data['name']}'
        AND description = '${data['description']}';
    `

    db.pool.query(create_sql, (error, rows, fields) => {
        if (error) {
            console.log(error);
            res.status(400).json({Error: error});
        } else {
            // get new id and send back
            db.pool.query(id_sql, (error, rows, fields) => {
                if (error) {
                    console.log(error);
                    res.status(400).json({Error: error});
                } else {
                    res.status(201).json(rows);
                }
            })
        }
    })
})

// update existing paymentType
router.put('/:paymentTypeID', (req, res) => {
    let paymentTypeID = parseInt(req.params.paymentTypeID);
    let data = req.body;
    let update_sql = `
        UPDATE PaymentTypes
        SET
            name = '${data['name']}',
            description = '${data['description']}'
        WHERE
            paymentTypeID = ${paymentTypeID};
    `
    db.pool.query(update_sql, (error, rows, fields) => {
        if (error) {
            console.log(error);
            res.status(400).json({Error: error});
        } else {
            res.status(200).json();
        }
    })
})

// delete existing paymentType
router.delete('/:paymentTypeID', (req, res) => {
    let paymentTypeID = parseInt(req.params.paymentTypeID);
    let delete_sql = `
        DELETE FROM PaymentTypes WHERE paymentTypeID = ${paymentTypeID};
    `
    db.pool.query(delete_sql, (error, rows, fields) => {
        if (error) {
            console.log(error);
            res.status(400).json({Error: error});
        } else {
            res.status(204).json()
        }
    })
})

module.exports = router;
