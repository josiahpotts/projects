const express = require('express')
const router = express.Router()

// Database
var db = require('../database/db-connector');

// get all customers
router.get('/', (req, res) => {
    let select_sql = `
        SELECT * FROM Customers;
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

// create new customer
router.post('/', (req, res) => {
    let data = req.body;
    let create_sql = `
        INSERT INTO Customers 
            (firstName, lastName, emailAddress, phoneNumber) 
        VALUES
            ('${data['firstName']}', '${data['lastName']}', '${data['emailAddress']}', '${data['phoneNumber']}');
    `
    let id_sql = `
        SELECT max(customerID) as customerID
        FROM Customers
        WHERE
            firstName = '${data['firstName']}'
        AND lastName = '${data['lastName']}'
        AND emailAddress = '${data['emailAddress']}'
        AND phoneNumber = '${data['phoneNumber']}';
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

// update existing customer
router.put('/:customerID', (req, res) => {
    let customerID = parseInt(req.params.customerID);
    let data = req.body;
    let update_sql = `
        UPDATE Customers
        SET
            firstName = '${data['firstName']}',
            lastName = '${data['lastName']}',
            emailAddress = '${data['emailAddress']}',
            phoneNumber = '${data['phoneNumber']}'
        WHERE
            customerID = ${customerID};
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

// delete existing customer
router.delete('/:customerID', (req, res) => {
    let customerID = parseInt(req.params.customerID);
    let delete_sql = `
        DELETE FROM Customers WHERE customerID = ${customerID};
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
