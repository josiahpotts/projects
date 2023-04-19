const express = require('express')
const router = express.Router()

// Database
var db = require('../database/db-connector');

// get all items
router.get('/', (req, res) => {
    let select_sql = `
        SELECT * FROM Items;
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

// create new item
router.post('/', (req, res) => {
    let data = req.body;
    let create_sql = `
        INSERT INTO Items 
            (name, price, description) 
        VALUES
            ('${data['name']}', '${data['price']}', '${data['description']}');
    `
    let id_sql = `
        SELECT max(itemID) as itemID
        FROM Items
        WHERE
            name = '${data['name']}'
        AND price = '${data['price']}'
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

// update existing item
router.put('/:itemID', (req, res) => {
    let itemID = parseInt(req.params.itemID);
    let data = req.body;
    let update_sql = `
        UPDATE Items
        SET
            name = '${data['name']}',
            price = '${data['price']}',
            description = '${data['description']}'
        WHERE
            itemID = ${itemID};
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

// delete existing item
router.delete('/:itemID', (req, res) => {
    let itemID = parseInt(req.params.itemID);
    let delete_sql = `
        DELETE FROM Items WHERE itemID = ${itemID};
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