import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CustomersPage from './pages/CustomersPage';
import EmployeesPage from './pages/EmployeesPage';
import PaymentTypesPage from './pages/PaymentTypesPage';
import ItemsPage from './pages/ItemsPage';
import SalesPage from './pages/SalesPage';
import RewardsPage from './pages/RewardsPage';

function App() {
  return (
    <div className="App">
        <Router>
          <Routes>
            <Route path="/" exact element={<HomePage />}></Route>
            <Route path="/customers" element={<CustomersPage />}></Route>
            <Route path="/employees" element={<EmployeesPage />}></Route>
            <Route path="/payment-types" element={<PaymentTypesPage />}></Route>
            <Route path="/items" element={<ItemsPage />}></Route>
            <Route path="/sales" element={<SalesPage />}></Route>
            <Route path="/rewards" element={<RewardsPage />}></Route>
          </Routes>
        </Router>
    </div>
  );
}

export default App;
