const express = require('express')
const router = express.Router()

// Database
var db = require('../database/db-connector');

// get all employees
router.get('/', (req, res) => {
    let select_sql = `
        SELECT * FROM Employees;
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

// create new employee
router.post('/', (req, res) => {
    let data = req.body;
    let create_sql = `
        INSERT INTO Employees 
            (firstName, lastName, title, hireDate) 
        VALUES
            ('${data['firstName']}', '${data['lastName']}', '${data['title']}', '${data['hireDate']}');
    `
    let id_sql = `
        SELECT max(employeeID) as employeeID
        FROM Employees
        WHERE
            firstName = '${data['firstName']}'
        AND lastName = '${data['lastName']}'
        AND title = '${data['title']}'
        AND hireDate = '${data['hireDate']}';
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

// update existing employee
router.put('/:employeeID', (req, res) => {
    let employeeID = parseInt(req.params.employeeID);
    let data = req.body;
    let update_sql = `
        UPDATE Employees
        SET
            firstName = '${data['firstName']}',
            lastName = '${data['lastName']}',
            title = '${data['title']}',
            hireDate = '${data['hireDate']}'
        WHERE
            employeeID = ${employeeID};
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

// delete existing employee
router.delete('/:employeeID', (req, res) => {
    let employeeID = parseInt(req.params.employeeID);
    let delete_sql = `
        DELETE FROM Employees WHERE employeeID = ${employeeID};
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
