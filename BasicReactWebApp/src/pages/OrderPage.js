import React from 'react';
import GroceryTable from '../components/GroceryTable.js'

function OrderPage({ items }) {
    return (
        <>
            <article>
                <h2>
                    Order some great things.
                </h2>
                <p>
                    Add up to 10 things each to your order.
                </p>
                <GroceryTable items={items}/>
            </article>
        </>
    );
}

export default OrderPage;