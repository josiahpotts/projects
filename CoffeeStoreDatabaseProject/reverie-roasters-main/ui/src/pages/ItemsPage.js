import React, { useState, useEffect } from 'react';
import { BiEditAlt, BiTrash } from 'react-icons/bi';
import Navigation from '../components/nav.js';


export const ItemsPage = () => {
    const [items, setItems] = useState([]);
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [description, setDescription] = useState('');
    const [editName, setEditName] = useState('');
    const [editPrice, setEditPrice] = useState('');
    const [editDescription, setEditDescription] = useState('');
    const [editItemID, setEditItemID] = useState('');
    

    const loadItems = async () => {
        console.log('getting items from db');
        const response = await fetch('/items');
        const items = await response.json();
        setItems(items);
    }

    const onAdd = async () => {
        // check for required fields
        if (!name) {
            alert('Name is required to create a new item.');
            return;
        }

        const newItem = {
            'name': name,
            'price' : price,
            'description': description,
        }
        const response = await fetch(`/items/`, {
            method: 'POST',
            body: JSON.stringify(newItem),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        const newItemID = result[0]['itemID'];
        
        if (response.status === 201) {
            alert("Successfully added new item!");
            newItem['itemID'] = newItemID;
            let newItems = items;
            newItems.push(newItem);
            setItems(newItems);
            
            // reset values
            setName('');
            setDescription('');
        } else {
            console.error(`Failed to add item, status code = ${response.status}`);
        };
    }

    const onDelete = async (itemID) => {
        const response = await fetch(`/items/${itemID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 204) {
            alert("Successfully deleted the item!");
            const newItems = items.filter(e => e.itemID !== itemID);
            setItems(newItems);
        } else {
            console.error(`Failed to delete item with id = ${itemID}, status code = ${response.status}`);
        };
    }

    const onEdit = async (item, i) => {
        setEditName(item.name);
        setEditPrice(item.price);
        setEditDescription(item.description);
        setEditItemID(item.itemID);
    };

    const onSave = async () => {
        // check for required fields
        if (!editName) {
            alert('Name cannot be blank.');
            return;
        }
        const updatedItem = {
            'name': editName,
            'description': editDescription,
        }
        const response = await fetch(`/items/${editItemID}`, {
            method: 'PUT',
            body: JSON.stringify(updatedItem),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 200) {
            alert("Successfully updated item!");
            updatedItem['itemID'] = editItemID;
            console.log(updatedItem, updatedItem.itemID);
            const updatedItems = [];
            console.log(items);
            for (const item of items) {
                console.log(item);
                if (item.itemID === updatedItem.itemID) {
                    updatedItems.push(updatedItem);
                } else {
                    updatedItems.push(item);
                }
            }
            console.log(updatedItems);
            setItems(updatedItems);
            
            // reset values
            setEditName('');
            setEditPrice('');
            setEditDescription('');
            setEditItemID('');
        } else {
            console.error(`Failed to add item, status code = ${response.status}`);
        };
    };

    useEffect(() => {
        loadItems();
    }, []);

    return (
        <>
            <h1>Items</h1>
            <Navigation />
            <table className="data-table" id="items-table">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>Item ID</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {items.map((item, i) => 
                <tr>
                    <td><button onClick={() => onEdit(item, i)}>< BiEditAlt /></button></td>
                    <td><button onClick={() => onDelete(item.itemID)}>< BiTrash /></button></td>
                    <td>{item.itemID}</td>
                    <td>{item.name}</td>
                    <td>{item.price}</td>
                    <td>{item.description}</td>
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
                <legend><strong>Add Item</strong></legend>
                    <fieldset>
                        <label> Name: </label> 
                            <input type="text" placeholder="" value={name} onChange={e => setName(e.target.value)} />
                        <label> Price: </label>
                            <input type="text" placeholder="" value={price} onChange={e => setPrice(e.target.value)} />
                        <label> Description: </label> 
                            <input type="text" placeholder="" value={description} onChange={e => setDescription(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onAdd} >Add</button>
            </div>

            <div>
                <legend><strong>Update Item</strong></legend>
                    <fieldset>
                        <input hidden type="text" value={editItemID} />
                        <label> Name: </label> 
                            <input type="text" placeholder="" value={editName} onChange={e => setEditName(e.target.value)} />
                        <label> Price: </label>
                            <input type="text" placeholder="" value={editPrice} onChange={e => setEditPrice(e.target.value)} />
                        <label> Description: </label> 
                            <input type="text" placeholder="" value={editDescription} onChange={e => setEditDescription(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onSave} >Save</button>
            </div>
        </>
    );
}

export default ItemsPage;