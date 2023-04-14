import React from 'react';
import StoreTable from '../components/StoreTable';
import ZipSearch from '../components/ZipSearch';

function StoresPage({ stores }) {
    return (
        <>
            <h2>
                Find your closest store location.
            </h2>
            <p>
                The form below will help you.
            </p>
            <StoreTable stores={stores} />
            <ZipSearch />
        </>
    );
}

export default StoresPage;