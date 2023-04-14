import React, { useState } from 'react';
import { MdNorth, MdSouth } from 'react-icons/md';

function SelectQuantity() {
    const [quantity, setQuantity] = useState(0);

    const increment = () => setQuantity(quantity === 10 ? quantity : quantity + 1);
    const decrement = () => setQuantity(quantity === 0 ? 0 : quantity - 1);

    return (
        <div>
            <MdSouth onClick={decrement} />
            <span>{quantity}</span>
            <MdNorth onClick={increment} />
        </div>
    );
}

export default SelectQuantity;