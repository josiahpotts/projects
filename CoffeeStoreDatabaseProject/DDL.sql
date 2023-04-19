SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

---
--- Table structure for table `Customers`
---
DROP TABLE IF EXISTS `Customers`;

CREATE TABLE `Customers` (
    customerID INT NOT NULL AUTO_INCREMENT,
    firstName varchar(255) DEFAULT NULL,
    lastName varchar(255) DEFAULT NULL,
    emailAddress varchar(255) NOT NULL,
    phoneNumber varchar(255) DEFAULT NULL,
    PRIMARY KEY (customerID),
    UNIQUE KEY (emailAddress)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `Customers`
---

--- LOCK TABLES `Customers` WRITE;

INSERT INTO `Customers` (firstName, lastName, emailAddress, phoneNumber) VALUES
("Eren", "Jaeger", "attacktitan@gmail.com", "111-111-1111"),
("Spongebob", "Squarepants", "bikinibottom@gmail.com", "123-456-7890"),
("Ragnar", "Lothbrook", "vikings@historychannel.com", "999-999-9999");

---
--- Table structure for table `Employees`
---
DROP TABLE IF EXISTS `Employees`;

CREATE TABLE `Employees` (
    employeeID INT NOT NULL AUTO_INCREMENT,
    firstName varchar(255) DEFAULT NULL,
    lastName varchar(255) NOT NULL,
    title varchar(255) NOT NULL,
    hireDate date NOT NULL,
    PRIMARY KEY (employeeID)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `Employees`
---

--- LOCK TABLES `Employees` WRITE;

INSERT INTO `Employees` (firstName, lastName, title, hireDate) VALUES
("Seto", "Kaiba", "Owner", '2000-02-27'),
("Frasier", "Crane", "Barista", '2010-06-25'),
("Master", "Yoda", "Cashier", "2015-11-20");

---
--- Table structure for table `PaymentTypes`
---
DROP TABLE IF EXISTS `PaymentTypes`;

CREATE TABLE `PaymentTypes` (
    paymentTypeID int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    description varchar(255) DEFAULT NULL,
    PRIMARY KEY (paymentTypeID)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `PaymentTypes`
---

--- LOCK TABLES `PaymentTypes` WRITE;

INSERT INTO `PaymentTypes` (name, description) VALUES
("Cash", "Customer paid in cash"),
("Debit", "Customer entered PIN for debit"),
("Credit", "Customer paid using credit");

---
--- Table structure for table `Sales`
---

DROP TABLE IF EXISTS `Sales`;

CREATE TABLE `Sales` (
    saleID int NOT NULL AUTO_INCREMENT,
    date datetime NOT NULL,
    total double NOT NULL,
    pointsEarned int(11) NOT NULL,
    pointsApplied int(11) DEFAULT 0,
    customerID int,
    paymentTypeID int NOT NULL,
    employeeID int,
    PRIMARY KEY (saleID),
    FOREIGN KEY (customerID) REFERENCES `Customers` (customerID) ON DELETE SET NULL,
    FOREIGN KEY (paymentTypeID) REFERENCES `PaymentTypes` (paymentTypeID) ON DELETE RESTRICT,
    FOREIGN KEY (employeeID) REFERENCES `Employees` (employeeID) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `Sales`
---

--- LOCK TABLES `Sales` WRITE;

INSERT INTO `Sales` (date, total, pointsEarned, pointsApplied, customerID, paymentTypeID, employeeID) VALUES
('2022-01-01', 10.99, 0, 0, (SELECT customerID FROM Customers WHERE firstName = "Eren"), (SELECT paymentTypeID FROM PaymentTypes WHERE name = "Cash"), (SELECT employeeID FROM Employees WHERE firstName = "Frasier")),
('2022-01-01', 14.99, 0, 0, (SELECT customerID FROM Customers WHERE firstName = "Spongebob"), (SELECT paymentTypeID FROM PaymentTypes WHERE name = "Credit"), (SELECT employeeID FROM Employees WHERE firstName = "Master")),
('2022-01-01', 9.95, 0, 0, (SELECT customerID FROM Customers WHERE firstName = "Ragnar"), (SELECT paymentTypeID FROM PaymentTypes WHERE name = "Debit"), (SELECT employeeID FROM Employees WHERE firstName = "Seto"));


---
--- Table structure for table `Rewards`
---
DROP TABLE IF EXISTS `Rewards`;

CREATE TABLE `Rewards` (
    rewardsPoints int DEFAULT 0,
    rewardsMemberSince date DEFAULT NULL,
    customerID int UNIQUE NOT NULL,

    FOREIGN KEY (customerID) REFERENCES `Customers` (customerID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `Rewards`
---

--- LOCK TABLES `Rewards` WRITE;

INSERT INTO `Rewards` (rewardsPoints, rewardsMemberSince, customerID) VALUES
(500, '2010-05-05', (SELECT customerID FROM Customers WHERE firstName = "Eren")),
(1500, '2010-03-05', (SELECT customerID FROM Customers WHERE firstName = "Ragnar")),
(0, '2010-10-15', (SELECT customerID FROM Customers WHERE firstName = "Spongebob"));

---
--- Table structure for table `Items`
---
DROP TABLE IF EXISTS `Items`;

CREATE TABLE `Items` (
    itemID int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    price double NOT NULL,
    description varchar(255) DEFAULT NULL,

    PRIMARY KEY (itemID)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `Items`
---

--- LOCK TABLES `Items` WRITE;

INSERT INTO `Items` (name, price, description) VALUES
("Chai Latte", 9.95, "Large hot chai with cinnamon"),
("Mocha", 10.99, "One shot espresso with chocolate syrup and milk"),
("Scone", 14.99, "Fresh baked chocolate chip scone");

---
--- Table structure for table `ItemSales`
---
DROP TABLE IF EXISTS `ItemSales`;

CREATE TABLE `ItemSales` (
    itemID int NOT NULL,
    saleID int NOT NULL,
    FOREIGN KEY (itemID) REFERENCES `Items` (itemID) ON DELETE CASCADE,
    FOREIGN KEY (saleID) REFERENCES `Sales` (saleID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

---
--- Dumping data for table `ItemSales`
---

--- LOCK TABLES `ItemSales` WRITE;

INSERT INTO `ItemSales` (itemID, saleID) VALUES
((SELECT itemID FROM Items WHERE name = "Chai Latte"), (SELECT saleID FROM Sales WHERE total = 9.95)),
((SELECT itemID FROM Items WHERE name = "Scone"), (SELECT saleID FROM Sales WHERE total = 14.99)),
((SELECT itemID FROM Items WHERE name = "Mocha"), (SELECT saleID FROM Sales WHERE total = 10.99));


SET FOREIGN_KEY_CHECKS=1;
COMMIT;