import React, { useState, useEffect } from 'react';
import { BiEditAlt, BiTrash } from 'react-icons/bi';
import Navigation from '../components/nav.js';


export const CustomersPage = () => {
    const [customers, setCustomers] = useState([]);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [emailAddress, setEmailAddress] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [editFirstName, setEditFirstName] = useState('');
    const [editLastName, setEditLastName] = useState('');
    const [editEmailAddress, setEditEmailAddress] = useState('');
    const [editPhoneNumber, setEditPhoneNumber] = useState('');
    const [editCustomerID, setEditCustomerID] = useState('');
    

    const loadCustomers = async () => {
        console.log('getting customers from db');
        const response = await fetch('/customers');
        const customers = await response.json();
        setCustomers(customers);
    }

    const onAdd = async () => {
        // check for required fields
        if (!emailAddress) {
            alert('Email Address is required to create a new customer.');
            return;
        }

        const newCustomer = {
            'firstName': firstName,
            'lastName': lastName,
            'emailAddress': emailAddress,
            'phoneNumber': phoneNumber
        }
        const response = await fetch(`/customers/`, {
            method: 'POST',
            body: JSON.stringify(newCustomer),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        const newCustomerID = result[0]['customerID'];
        
        if (response.status === 201) {
            alert("Successfully added new customer!");
            newCustomer['customerID'] = newCustomerID;
            let newCustomers = customers;
            newCustomers.push(newCustomer);
            setCustomers(newCustomers);
            
            // reset values
            setFirstName('');
            setLastName('');
            setEmailAddress('');
            setPhoneNumber('');
        } else {
            console.error(`Failed to add customer, status code = ${response.status}`);
        };
    }

    const onDelete = async (customerID) => {
        const response = await fetch(`/customers/${customerID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 204) {
            alert("Successfully deleted the customer!");
            const newCustomers = customers.filter(e => e.customerID !== customerID);
            setCustomers(newCustomers);
        } else {
            console.error(`Failed to delete customer with id = ${customerID}, status code = ${response.status}`);
        };
    }

    const onEdit = async (customer, i) => {
        setEditFirstName(customer.firstName);
        setEditLastName(customer.lastName);
        setEditEmailAddress(customer.emailAddress);
        setEditPhoneNumber(customer.phoneNumber);
        setEditCustomerID(customer.customerID);
    };

    const onSave = async () => {
        // check for required fields
        if (!editEmailAddress) {
            alert('Email Address cannot be blank.');
            return;
        }
        const updatedCustomer = {
            'firstName': editFirstName,
            'lastName': editLastName,
            'emailAddress': editEmailAddress,
            'phoneNumber': editPhoneNumber
        }
        const response = await fetch(`/customers/${editCustomerID}`, {
            method: 'PUT',
            body: JSON.stringify(updatedCustomer),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 200) {
            alert("Successfully updated customer!");
            updatedCustomer['customerID'] = editCustomerID;
            console.log(updatedCustomer, updatedCustomer.customerID);
            const updatedCustomers = [];
            console.log(customers);
            for (const customer of customers) {
                console.log(customer);
                if (customer.customerID === updatedCustomer.customerID) {
                    updatedCustomers.push(updatedCustomer);
                } else {
                    updatedCustomers.push(customer);
                }
            }
            console.log(updatedCustomers);
            setCustomers(updatedCustomers);
            
            // reset values
            setEditFirstName('');
            setEditLastName('');
            setEditEmailAddress('');
            setEditPhoneNumber('');
            setEditCustomerID('');
        } else {
            console.error(`Failed to add customer, status code = ${response.status}`);
        };
    };

    useEffect(() => {
        loadCustomers();
    }, []);

    return (
        <>
            <h1>Customers</h1>
            <Navigation />
            <table className="data-table" id="customers-table">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>Customer ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Email Address</th>
                    <th>Phone Number</th>
                </tr>
            </thead>
            <tbody>
                {customers.map((customer, i) => 
                <tr>
                    <td><button onClick={() => onEdit(customer, i)}>< BiEditAlt /></button></td>
                    <td><button onClick={() => onDelete(customer.customerID)}>< BiTrash /></button></td>
                    <td>{customer.customerID}</td>
                    <td>{customer.firstName}</td>
                    <td>{customer.lastName}</td>
                    <td>{customer.emailAddress}</td>
                    <td>{customer.phoneNumber}</td>
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
                <legend><strong>Add Customer</strong></legend>
                    <fieldset>
                        <label> First Name: </label> 
                            <input type="text" placeholder="" value={firstName} onChange={e => setFirstName(e.target.value)} />
                        <label> Last Name: </label> 
                            <input type="text" placeholder="" value={lastName} onChange={e => setLastName(e.target.value)} />
                        <p></p>
                        <label> Email Address: </label> 
                            <input type="text" placeholder="" value={emailAddress} onChange={e => setEmailAddress(e.target.value)} required/>
                        <label> Phone Number: </label> 
                        <input type="text" placeholder="" value={phoneNumber} onChange={e => setPhoneNumber(e.target.value)} />
                    </fieldset>
                <button onClick={onAdd} >Add</button>
            </div>

            <div>
                <legend><strong>Update Customer</strong></legend>
                    <fieldset>
                        <input hidden type="text" value={editCustomerID} />
                        <label> First Name: </label> 
                            <input type="text" placeholder="" value={editFirstName} onChange={e => setEditFirstName(e.target.value)} />
                        <label> Last Name: </label> 
                            <input type="text" placeholder="" value={editLastName} onChange={e => setEditLastName(e.target.value)} />
                        <p></p>
                        <label> Email Address: </label> 
                            <input type="text" placeholder="" value={editEmailAddress} onChange={e => setEditEmailAddress(e.target.value)} required/>
                        <label> Phone Number: </label> 
                        <input type="text" placeholder="" value={editPhoneNumber} onChange={e => setEditPhoneNumber(e.target.value)} />
                    </fieldset>
                <button onClick={onSave} >Save</button>
            </div>
        </>
    );
}

export default CustomersPage;
