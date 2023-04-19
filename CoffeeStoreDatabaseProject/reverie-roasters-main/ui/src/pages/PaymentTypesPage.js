import React, { useState, useEffect } from 'react';
import { BiEditAlt, BiTrash } from 'react-icons/bi';
import Navigation from '../components/nav.js';


export const PaymentTypesPage = () => {
    const [paymentTypes, setPaymentTypes] = useState([]);
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [editName, setEditName] = useState('');
    const [editDescription, setEditDescription] = useState('');
    const [editPaymentTypeID, setEditPaymentTypeID] = useState('');
    

    const loadPaymentTypes = async () => {
        console.log('getting paymentTypes from db');
        const response = await fetch('/paymentTypes');
        const paymentTypes = await response.json();
        setPaymentTypes(paymentTypes);
    }

    const onAdd = async () => {
        // check for required fields
        if (!name) {
            alert('Name is required to create a new paymentType.');
            return;
        }

        const newPaymentType = {
            'name': name,
            'description': description,
        }
        const response = await fetch(`/paymentTypes/`, {
            method: 'POST',
            body: JSON.stringify(newPaymentType),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        const newPaymentTypeID = result[0]['paymentTypeID'];
        
        if (response.status === 201) {
            alert("Successfully added new paymentType!");
            newPaymentType['paymentTypeID'] = newPaymentTypeID;
            let newPaymentTypes = paymentTypes;
            newPaymentTypes.push(newPaymentType);
            setPaymentTypes(newPaymentTypes);
            
            // reset values
            setName('');
            setDescription('');
        } else {
            console.error(`Failed to add paymentType, status code = ${response.status}`);
        };
    }

    const onDelete = async (paymentTypeID) => {
        const response = await fetch(`/paymentTypes/${paymentTypeID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 204) {
            alert("Successfully deleted the paymentType!");
            const newPaymentTypes = paymentTypes.filter(e => e.paymentTypeID !== paymentTypeID);
            setPaymentTypes(newPaymentTypes);
        } else {
            console.error(`Failed to delete paymentType with id = ${paymentTypeID}, status code = ${response.status}`);
        };
    }

    const onEdit = async (paymentType, i) => {
        setEditName(paymentType.name);
        setEditDescription(paymentType.description);
        setEditPaymentTypeID(paymentType.paymentTypeID);
    };

    const onSave = async () => {
        // check for required fields
        if (!editName) {
            alert('Name cannot be blank.');
            return;
        }
        const updatedPaymentType = {
            'name': editName,
            'description': editDescription,
        }
        const response = await fetch(`/paymentTypes/${editPaymentTypeID}`, {
            method: 'PUT',
            body: JSON.stringify(updatedPaymentType),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 200) {
            alert("Successfully updated paymentType!");
            updatedPaymentType['paymentTypeID'] = editPaymentTypeID;
            console.log(updatedPaymentType, updatedPaymentType.paymentTypeID);
            const updatedPaymentTypes = [];
            console.log(paymentTypes);
            for (const paymentType of paymentTypes) {
                console.log(paymentType);
                if (paymentType.paymentTypeID === updatedPaymentType.paymentTypeID) {
                    updatedPaymentTypes.push(updatedPaymentType);
                } else {
                    updatedPaymentTypes.push(paymentType);
                }
            }
            console.log(updatedPaymentTypes);
            setPaymentTypes(updatedPaymentTypes);
            
            // reset values
            setEditName('');
            setEditDescription('');
            setEditPaymentTypeID('');
        } else {
            console.error(`Failed to add paymentType, status code = ${response.status}`);
        };
    };

    useEffect(() => {
        loadPaymentTypes();
    }, []);

    return (
        <>
            <h1>PaymentTypes</h1>
            <Navigation />
            <table className="data-table" id="paymentTypes-table">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>PaymentType ID</th>
                    <th>Name</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {paymentTypes.map((paymentType, i) => 
                <tr>
                    <td><button onClick={() => onEdit(paymentType, i)}>< BiEditAlt /></button></td>
                    <td><button onClick={() => onDelete(paymentType.paymentTypeID)}>< BiTrash /></button></td>
                    <td>{paymentType.paymentTypeID}</td>
                    <td>{paymentType.name}</td>
                    <td>{paymentType.description}</td>
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
                <legend><strong>Add PaymentType</strong></legend>
                    <fieldset>
                        <label> Name: </label> 
                            <input type="text" placeholder="" value={name} onChange={e => setName(e.target.value)} />
                        <label> Description: </label> 
                            <input type="text" placeholder="" value={description} onChange={e => setDescription(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onAdd} >Add</button>
            </div>

            <div>
                <legend><strong>Update PaymentType</strong></legend>
                    <fieldset>
                        <input hidden type="text" value={editPaymentTypeID} />
                        <label> Name: </label> 
                            <input type="text" placeholder="" value={editName} onChange={e => setEditName(e.target.value)} />
                        <label> Description: </label> 
                            <input type="text" placeholder="" value={editDescription} onChange={e => setEditDescription(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onSave} >Save</button>
            </div>
        </>
    );
}

export default PaymentTypesPage;