/* ==============
   - Josiah Potts
   - Tyler Eto
   ============== */

/* =====
   Sales
   ===== */

-- Query to get sales
SELECT 
    s.saleID,
    s.date,
    s.customerID,
    CONCAT(IFNULL(c.firstName, ''), ' ', IFNULL(c.lastName, '')),
    s.total,
    s.pointsEarned,
    s.pointsApplied,
    s.employeeID,
    CONCAT(IFNULL(e.firstName, ''), ' ', IFNULL(e.lastName, '')),
    s.paymentTypeID,
    pt.name
FROM Sales s
    LEFT JOIN Customers c ON s.customerID = c.customerID
    LEFT JOIN Employees e ON s.employeeID = e.employeeID
    LEFT JOIN PaymentTypes pt ON s.paymentTypeID = pt.paymentTypeID
;

-- Query to add a new sale event
INSERT INTO Sales
    (date, total, pointsEarned, pointsApplied, customerID, paymentTypeID, employeeID)
VALUES
    (:sdate, :total, :rewardsearned, :rewardsapplied, :CustomerID, :PaymentTypeID, :EmployeeID)
;

-- Query to update an existing sale
UPDATE Sales
SET
    date = :sdate, 
    customerID = :CustomerID,
    total = :total,
    pointsEarned = :rewardsearned,
    pointsApplied = :rewardsapplied,
    paymentTypeID = :PaymentTypeID,
    employeeID = :EmployeeID
WHERE
    saleID = :SaleID
;

-- Query to delete an existing sale
DELETE FROM Sales WHERE saleID = :SaleID;

-- Query to add an item to sale
INSERT INTO ItemSales
    (itemID, saleID)
VALUES
    (:ItemID, :SaleID)
;

-- Query to delete an item from sale
DELETE 
    FROM ItemSales 
WHERE 
    itemID = :ItemID
AND saleID = :SaleID
;


/* =========
   Customers
   ========= */

-- Query to get customers
SELECT * FROM Customers;

-- Query to add a new customer
INSERT INTO Customers 
    (firstName, lastName, emailAddress, phoneNumber) 
VALUES
    (:fname, :lname, :email, :phone)
;

-- Query to update existing customer
UPDATE Customer
SET 
    firstName = :fname,
    lastName = :lname,
    emailAddress = :email,
    phoneNumber = :phone
WHERE 
    customerID = :customerID
;

-- Query to delete existing customer
DELETE FROM Customer WHERE customerID = :CustomerID;


/* =========
   Employees
   ========= */

-- Query to get employees
SELECT * FROM Employees;

-- Query to add a new employee
INSERT INTO Employees
    (firstName, lastName, title, hireDate) 
VALUES
    (:fname, :lname, :jtitle, :hdate)
;

-- Query to update existing employee
UPDATE Employees
SET 
    firstName = :fname,
    lastName = :lname,
    title = :jtitle,
    hireDate = :hdate
WHERE 
    employeeID = :EmployeeID
;

-- Query to delete existing employee
DELETE FROM Employees WHERE employeeID = :EmployeeID;


/* =====
   Items
   ===== */

-- Query to get items
SELECT * FROM Items;

-- Query to look up item by name
SELECT * 
FROM Items 
WHERE
    name LIKE "%:name%"
;

-- Query to add a new item
INSERT INTO Items
    (name, price, description)
VALUES
    (:name, :price, :description)
;

-- Query to update existing item
UPDATE Items
SET
    name = :name,
    price = :price,
    description = :description
WHERE
    itemID = :ItemID
;

-- Query to delete existing item
DELETE FROM Items WHERE itemID = :ItemID;


/* ============
   PaymentTypes
   ============ */

-- Query to get payment types
SELECT * FROM PaymentTypes;

-- Query to add a new payment type
INSERT INTO PaymentTypes
    (name, description)
VALUES
    (:name, :description)
;

-- Query to update existing payment type
UPDATE PaymentTypes
SET
    name = :name,
    description = :description
WHERE
    paymentTypeID = :PaymentTypeID
;

-- Query to delete existing payment type
DELETE FROM PaymentTypes WHERE paymentTypeID = :PaymentTypeID;


/* =======
   Rewards
   ======= */

-- Query to get rewards
SELECT 
    r.customerID, 
    CONCAT(IFNULL(c.firstName, ''), ' ', IFNULL(c.lastName, '')),
    r.rewardsMemberSince,
    r.rewardsPoints
FROM Rewards r
    JOIN Customers c ON c.customerID = r.customerID
;

-- Query to add a new rewards member
INSERT INTO Rewards
    (rewardsPoints, rewardsMemberSince, customerID)
VALUES
    (:points, :rdate, :CustomerID)
;

-- Query to update existing rewards member
UPDATE Rewards
SET
    rewardsPoints = :points,
    rewardsMemberSince = :rdate
WHERE
    customerID = :CustomerID
;

-- Query to delete existing rewards member
DELETE FROM Rewards WHERE customerID = :CustomerID;

/* =========
   ItemSales
   ========= */

-- Query to add an item to sale
INSERT INTO ItemSales
    (itemID, saleID)
VALUES
    (:ItemID, :SaleID)
;

-- Query to delete an item from sale
DELETE 
    FROM ItemSales 
WHERE 
    itemID = :ItemID
AND saleID = :SaleID
;
