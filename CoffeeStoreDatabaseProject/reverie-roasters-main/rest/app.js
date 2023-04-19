/*
    SETUP
*/

// express
var express = require('express');
var app = express();
PORT = 61021;

// load routes
const customers = require('./routes/customers');
const employees = require('./routes/employees');
const paymentTypes = require('./routes/paymentTypes');
const items = require('./routes/items');
const sales = require('./routes/sales');
const rewards = require('./routes/rewards');

// assign middleware
app.use(express.urlencoded({extended: true}));
app.use(express.json());
app.use('/customers', customers);
app.use('/employees', employees);
app.use('/paymentTypes', paymentTypes);
app.use('/items', items);
app.use('/sales', sales);
app.use('/rewards', rewards);


/*
    LISTENER
*/
app.listen(PORT, function(){
    console.log('Express started on http://localhost:' + PORT + '; press Ctrl-C to terminate.')
});
