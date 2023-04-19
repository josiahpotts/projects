import React, { useState, useEffect } from 'react';
import { BiEditAlt, BiTrash } from 'react-icons/bi';
import Navigation from '../components/nav.js';


export const SalesPage = () => {
    const [sales, setSales] = useState([]);
    const [date, setDate] = useState('');
    const [total, setTotal] = useState('');
    const [pointsEarned, setPointsEarned] = useState('');
    const [pointsApplied, setPointsApplied] = useState('');
    const [customerID, setCustomerID] = useState('');
    const [paymentTypeID, setPaymentTypeID] = useState('');
    const [employeeID, setEmployeeID] = useState('');
    const [editDate, setEditDate] = useState('');
    const [editTotal, setEditTotal] = useState('');
    const [editPointsEarned, setEditPointsEarned] = useState('');
    const [editPointsApplied, setEditPointsApplied] = useState('');
    const [editCustomerID, setEditCustomerID] = useState('');
    const [editPaymentTypeID, setEditPaymentTypeID] = useState('');
    const [editEmployeeID, setEditEmployeeID] = useState(''); 
    const [editSaleID, setEditSaleID] = useState('');
    const [customers, setCustomers] = useState([]);
    

    const loadSales = async () => {
        console.log('getting sales from db');
        const response = await fetch('/sales');
        const sales = await response.json();
        setSales(sales);
    }

    const onAdd = async () => {
        // check for required fields
        if (!total) {
            alert('Total is required to create a new sale.');
            return;
        }

        const newSale = {
            'date': date,
            'total': total,
            'pointsEarned': pointsEarned,
            'pointsApplied': pointsApplied,
            'customerID' : customerID,
            'paymentTypeID' : paymentTypeID,
            'employeeID' : employeeID
        }
        const response = await fetch(`/sales/`, {
            method: 'POST',
            body: JSON.stringify(newSale),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        const newSaleID = result[0]['saleID'];
        
        if (response.status === 201) {
            alert("Successfully added new sale!");
            newSale['saleID'] = newSaleID;
            let newSales = sales;
            newSales.push(newSale);
            setSales(newSales);
            
            // reset values
            setDate('');
            setTotal('');
            setPointsEarned('');
            setPointsApplied('');
            setCustomerID('');
            setPaymentTypeID('');
            setEmployeeID('');
        } else {
            console.error(`Failed to add sale, status code = ${response.status}`);
        };
    }

    const loadCustomers = async () => {
        const response = await fetch(`/customers`);
        const customers = await response.json();
        setCustomers(customers)
    }

    const onDelete = async (saleID) => {
        const response = await fetch(`/sales/${saleID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 204) {
            alert("Successfully deleted the sale!");
            const newSales = sales.filter(e => e.saleID !== saleID);
            setSales(newSales);
        } else {
            console.error(`Failed to delete sale with id = ${saleID}, status code = ${response.status}`);
        };
    }

    const onEdit = async (sale, i) => {
        setEditDate(sale.date);
        setEditTotal(sale.total);
        setEditPointsEarned(sale.pointsEarned);
        setEditPointsApplied(sale.pointsApplied);
        setEditCustomerID(sale.customerID);
        setEditPaymentTypeID(sale.paymentTypeID);
        setEditEmployeeID(sale.employeeID);
        setEditSaleID(sale.saleID);
    };

    const onSave = async () => {
        // check for required fields
        if (!editPointsEarned) {
            alert('Points Earned cannot be blank.');
            return;
        }
        const updatedSale = {
            'date': editDate,
            'total': editTotal,
            'pointsEarned': editPointsEarned,
            'pointsApplied': editPointsApplied,
            'customerID' : customerID,
            'paymentTypeID' : paymentTypeID,
            'employeeID' : employeeID
        }
        const response = await fetch(`/sales/${editSaleID}`, {
            method: 'PUT',
            body: JSON.stringify(updatedSale),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 200) {
            alert("Successfully updated sale!");
            updatedSale['saleID'] = editSaleID;
            console.log(updatedSale, updatedSale.saleID);
            const updatedSales = [];
            console.log(sales);
            for (const sale of sales) {
                console.log(sale);
                if (sale.saleID === updatedSale.saleID) {
                    updatedSales.push(updatedSale);
                } else {
                    updatedSales.push(sale);
                }
            }
            console.log(updatedSales);
            setSales(updatedSales);
            
            // reset values
            setEditDate('');
            setEditTotal('');
            setEditPointsEarned('');
            setEditPointsApplied('');
            setEditCustomerID('');
            setEditPaymentTypeID('');
            setEditEmployeeID('');
            setEditSaleID('');
        } else {
            console.error(`Failed to add sale, status code = ${response.status}`);
        };
    };

    useEffect(() => {
        loadSales();
    }, []);

    return (
        <>
            <h1>Sales</h1>
            <Navigation />
            <table className="data-table" id="sales-table">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>Sale ID</th>
                    <th>Date</th>
                    <th>Total</th>
                    <th>Points Earned</th>
                    <th>Points Applied</th>
                    <th>Customer ID</th>
                    <th>Payment Type ID</th>
                    <th>Employee ID</th>
                </tr>
            </thead>
            <tbody>
                {sales.map((sale, i) => 
                <tr>
                    <td><button onClick={() => onEdit(sale, i)}>< BiEditAlt /></button></td>
                    <td><button onClick={() => onDelete(sale.saleID)}>< BiTrash /></button></td>
                    <td>{sale.saleID}</td>
                    <td>{sale.date}</td>
                    <td>{sale.total}</td>
                    <td>{sale.pointsEarned}</td>
                    <td>{sale.pointsApplied}</td>
                    <td>{sale.customerID}</td>
                    <td>{sale.paymentTypeID}</td>
                    <td>{sale.employeeID}</td>
                </tr>
                )}
            </tbody>
            </table>
            
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>

            <div>
                <legend><strong>Add Sale</strong></legend>
                    <fieldset>
                        <label> Date: </label> 
                            <input type="text" placeholder="" value={date} onChange={e => setDate(e.target.value)} />
                        <label> Total: </label> 
                            <input type="text" placeholder="" value={total} onChange={e => setTotal(e.target.value)} />
                        <label> Points Earned: </label> 
                            <input type="text" placeholder="" value={pointsEarned} onChange={e => setPointsEarned(e.target.value)} required/>
                        <label> Points Applied: </label> 
                            <input type="text" placeholder="" value={pointsApplied} onChange={e => setPointsApplied(e.target.value)} />
                        <label> Customer ID: </label> 
                            <input type="text" placeholder="" value={customerID} onChange={e => setCustomerID(e.target.value)} />
                        <label> Payment Type ID: </label> 
                            <input type="text" placeholder="" value={paymentTypeID} onChange={e => setPaymentTypeID(e.target.value)} />
                        <label> Employee ID: </label> 
                            <input type="text" placeholder="" value={employeeID} onChange={e => setEmployeeID(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onAdd} >Add</button>
            </div>

            <div>
                <legend><strong>Update Sale</strong></legend>
                    <fieldset>
                        <input hidden type="text" value={editSaleID} />
                        <label> Date: </label> 
                            <input type="text" placeholder="" value={editDate} onChange={e => setEditDate(e.target.value)} />
                        <label> Total: </label> 
                            <input type="text" placeholder="" value={editTotal} onChange={e => setEditTotal(e.target.value)} />
                        <label> Points Earned: </label> 
                            <input type="text" placeholder="" value={editPointsEarned} onChange={e => setEditPointsEarned(e.target.value)} required/>
                        <label> Points Applied: </label> 
                            <input type="text" placeholder="" value={editPointsApplied} onChange={e => setEditPointsApplied(e.target.value)} />
                        <label> Customer ID: </label> 
                            <input type="text" placeholder="" value={editCustomerID} onChange={e => setCustomerID(e.target.value)} />
                        <label> Payment Type ID: </label> 
                            <input type="text" placeholder="" value={editPaymentTypeID} onChange={e => setPaymentTypeID(e.target.value)} />
                        <label> Employee ID: </label> 
                            <input type="text" placeholder="" value={editEmployeeID} onChange={e => setEmployeeID(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onSave} >Save</button>
            </div>
        </>
    );
}

export default SalesPage;