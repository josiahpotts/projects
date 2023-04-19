import React, { useState, useEffect } from 'react';
import { BiEditAlt, BiTrash } from 'react-icons/bi';
import Navigation from '../components/nav.js';


export const EmployeesPage = () => {
    const [employees, setEmployees] = useState([]);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [title, setTitle] = useState('');
    const [hireDate, setHireDate] = useState('');
    const [editFirstName, setEditFirstName] = useState('');
    const [editLastName, setEditLastName] = useState('');
    const [editTitle, setEditTitle] = useState('');
    const [editHireDate, setEditHireDate] = useState('');
    const [editEmployeeID, setEditEmployeeID] = useState('');
    

    const loadEmployees = async () => {
        console.log('getting employees from db');
        const response = await fetch('/employees');
        const employees = await response.json();
        setEmployees(employees);
    }

    const onAdd = async () => {
        // check for required fields
        if (!title) {
            alert('Title is required to create a new employee.');
            return;
        }

        const newEmployee = {
            'firstName': firstName,
            'lastName': lastName,
            'title': title,
            'hireDate': hireDate
        }
        const response = await fetch(`/employees/`, {
            method: 'POST',
            body: JSON.stringify(newEmployee),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        const newEmployeeID = result[0]['employeeID'];
        
        if (response.status === 201) {
            alert("Successfully added new employee!");
            newEmployee['employeeID'] = newEmployeeID;
            let newEmployees = employees;
            newEmployees.push(newEmployee);
            setEmployees(newEmployees);
            
            // reset values
            setFirstName('');
            setLastName('');
            setTitle('');
            setHireDate('');
        } else {
            console.error(`Failed to add employee, status code = ${response.status}`);
        };
    }

    const onDelete = async (employeeID) => {
        const response = await fetch(`/employees/${employeeID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 204) {
            alert("Successfully deleted the employee!");
            const newEmployees = employees.filter(e => e.employeeID !== employeeID);
            setEmployees(newEmployees);
        } else {
            console.error(`Failed to delete employee with id = ${employeeID}, status code = ${response.status}`);
        };
    }

    const onEdit = async (employee, i) => {
        setEditFirstName(employee.firstName);
        setEditLastName(employee.lastName);
        setEditTitle(employee.title);
        setEditHireDate(employee.hireDate);
        setEditEmployeeID(employee.employeeID);
    };

    const onSave = async () => {
        // check for required fields
        if (!editTitle) {
            alert('Title cannot be blank.');
            return;
        }
        const updatedEmployee = {
            'firstName': editFirstName,
            'lastName': editLastName,
            'title': editTitle,
            'hireDate': editHireDate
        }
        const response = await fetch(`/employees/${editEmployeeID}`, {
            method: 'PUT',
            body: JSON.stringify(updatedEmployee),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 200) {
            alert("Successfully updated employee!");
            updatedEmployee['employeeID'] = editEmployeeID;
            console.log(updatedEmployee, updatedEmployee.employeeID);
            const updatedEmployees = [];
            console.log(employees);
            for (const employee of employees) {
                console.log(employee);
                if (employee.employeeID === updatedEmployee.employeeID) {
                    updatedEmployees.push(updatedEmployee);
                } else {
                    updatedEmployees.push(employee);
                }
            }
            console.log(updatedEmployees);
            setEmployees(updatedEmployees);
            
            // reset values
            setEditFirstName('');
            setEditLastName('');
            setEditTitle('');
            setEditHireDate('');
            setEditEmployeeID('');
        } else {
            console.error(`Failed to add employee, status code = ${response.status}`);
        };
    };

    useEffect(() => {
        loadEmployees();
    }, []);

    return (
        <>
            <h1>Employees</h1>
            <Navigation />
            <table className="data-table" id="employees-table">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>Employee ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Title</th>
                    <th>Hire Date</th>
                </tr>
            </thead>
            <tbody>
                {employees.map((employee, i) => 
                <tr>
                    <td><button onClick={() => onEdit(employee, i)}>< BiEditAlt /></button></td>
                    <td><button onClick={() => onDelete(employee.employeeID)}>< BiTrash /></button></td>
                    <td>{employee.employeeID}</td>
                    <td>{employee.firstName}</td>
                    <td>{employee.lastName}</td>
                    <td>{employee.title}</td>
                    <td>{employee.hireDate}</td>
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
                <legend><strong>Add Employee</strong></legend>
                    <fieldset>
                        <label> First Name: </label> 
                            <input type="text" placeholder="" value={firstName} onChange={e => setFirstName(e.target.value)} />
                        <label> Last Name: </label> 
                            <input type="text" placeholder="" value={lastName} onChange={e => setLastName(e.target.value)} />
                        <p></p>
                        <label> Title: </label> 
                            <input type="text" placeholder="" value={title} onChange={e => setTitle(e.target.value)} required/>
                        <label> Hire Date: </label> 
                        <input type="text" placeholder="" value={hireDate} onChange={e => setHireDate(e.target.value)} />
                    </fieldset>
                <button onClick={onAdd} >Add</button>
            </div>

            <div>
                <legend><strong>Update Employee</strong></legend>
                    <fieldset>
                        <input hidden type="text" value={editEmployeeID} />
                        <label> First Name: </label> 
                            <input type="text" placeholder="" value={editFirstName} onChange={e => setEditFirstName(e.target.value)} />
                        <label> Last Name: </label> 
                            <input type="text" placeholder="" value={editLastName} onChange={e => setEditLastName(e.target.value)} />
                        <p></p>
                        <label> Title: </label> 
                            <input type="text" placeholder="" value={editTitle} onChange={e => setEditTitle(e.target.value)} required/>
                        <label> Hire Date: </label> 
                        <input type="text" placeholder="" value={editHireDate} onChange={e => setEditHireDate(e.target.value)} />
                    </fieldset>
                <button onClick={onSave} >Save</button>
            </div>
        </>
    );
}

export default EmployeesPage;