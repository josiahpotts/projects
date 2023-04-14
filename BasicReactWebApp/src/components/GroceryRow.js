import React from 'react';
import SelectQuantity from './SelectQuantity.js';

function GroceryRow({ item }) {
    return (
        <tr>
            <td>{item.name}</td>
            <td>${item.price}</td>
            <td><SelectQuantity /></td>
        </tr>
    );
}

export default GroceryRow;