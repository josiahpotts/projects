import './App.css';
import stores from './data/stores.js';
import items from './data/items.js';
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import StoresPage from './pages/StoresPage';
import HomePage from './pages/HomePage';
import OrderPage from './pages/OrderPage';

import Navigation from './components/nav.js';

import { MdShoppingBasket } from 'react-icons/md'

function App() {

  return (
    <div>
      <Router>
        <header>
          <h1>
            Randomly Assorted Inventory Store
          </h1>
            <MdShoppingBasket />
          <p>
            Where we sell you items that are randomly given to us by the owner.
          </p>
        </header>
        <Navigation />
        <main>
          <article>
            <Route path="/(|index.html)" exact><HomePage /></Route>
            <Route path="/order"><OrderPage items={items} /></Route>
            <Route path="/stores"><StoresPage stores={stores} /></Route>
          </article>
        </main>
        <footer>
          <p>Modified on {Date()}. <cite>&copy; 2022 Josiah Potts</cite>.</p>
        </footer>
      </Router>
    </div>
  );
}

export default App;
