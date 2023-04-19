const express = require('express')
const router = express.Router()

// Database
var db = require('../database/db-connector');

// get all rewards
router.get('/', (req, res) => {
    let select_sql = `
        SELECT * FROM Rewards;
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

// create new reward
router.post('/', (req, res) => {
    let data = req.body;
    let create_sql = `
        INSERT INTO Rewards 
            (rewardsPoints, rewardsMemberSince, customerID) 
        VALUES
            ('${data['rewardsPoints']}', '${data['rewardsMemberSince']}', '${data['customerID']}');
    `
    let id_sql = `
        SELECT max(customerID) as customerID
        FROM Rewards
        WHERE
            rewardsPoints = '${data['rewardsPoints']}'
        AND rewardsMemberSince = '${data['rewardsMemberSince']}'
        AND customerID = '${data['customerID']}';
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

// update existing reward
router.put('/:customerID', (req, res) => {
    let customerID = parseInt(req.params.customerID);
    let data = req.body;
    let update_sql = `
        UPDATE Rewards
        SET
            rewardsPoints = '${data['rewardsPoints']}',
            rewardsMemberSince = '${data['rewardsMemberSince']}',
            customerID = '${data['customerID']}'
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

// delete existing reward
router.delete('/:customerID', (req, res) => {
    let customerID = parseInt(req.params.customerID);
    let delete_sql = `
        DELETE FROM Rewards WHERE customerID = ${customerID};
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