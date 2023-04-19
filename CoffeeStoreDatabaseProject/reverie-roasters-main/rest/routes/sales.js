const express = require('express')
const router = express.Router()

// Database
var db = require('../database/db-connector');

// get all sales
router.get('/', (req, res) => {
    let select_sql = `
        SELECT * FROM Sales;
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

// create new sale
router.post('/', (req, res) => {
    let data = req.body;
    let create_sql = `
        INSERT INTO Sales 
            (date, total, pointsEarned, pointsApplied, customerID, paymentTypeID, employeeID) 
        VALUES
            ('${data['date']}', '${data['total']}', '${data['pointsEarned']}', '${data['pointsApplied']}', '${data['customerID']}', '${data['paymentTypeID']}', '${data['employeeID']}');
    `
    let id_sql = `
        SELECT max(saleID) as saleID
        FROM Sales
        WHERE
            date = '${data['date']}'
        AND total = '${data['total']}'
        AND pointsEarned = '${data['pointsEarned']}'
        AND pointsApplied = '${data['pointsApplied']}'
        AND customerID = '${data['customerID']}'
        AND paymentTypeID = '${data['paymentTypeID']}'
        AND employeeID = '${data['employeeID']}';
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

// update existing sale
router.put('/:saleID', (req, res) => {
    let saleID = parseInt(req.params.saleID);
    let data = req.body;
    let update_sql = `
        UPDATE Sales
        SET
            date = '${data['date']}',
            total = '${data['total']}',
            pointsEarned = '${data['pointsEarned']}',
            pointsApplied = '${data['pointsApplied']}'
        WHERE
            saleID = ${saleID};
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

// delete existing sale
router.delete('/:saleID', (req, res) => {
    let saleID = parseInt(req.params.saleID);
    let delete_sql = `
        DELETE FROM Sales WHERE saleID = ${saleID};
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
