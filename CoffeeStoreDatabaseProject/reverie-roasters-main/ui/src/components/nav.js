import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
    return (
        <nav>
            <Link to="/">Home</Link>
            <Link to="../customers"> Customers </Link>
            <Link to="../employees"> Employees </Link>
            <Link to="../payment-types"> Payment Types </Link>
            <Link to="../items"> Items </Link>
            <Link to="../sales"> Sales </Link>
            <Link to="../rewards"> Rewards </Link>
        </nav>
    );
}

export default Navigation;