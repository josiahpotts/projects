import React, { useState, useEffect } from 'react';
import { BiEditAlt, BiTrash } from 'react-icons/bi';
import Navigation from '../components/nav.js';


export const RewardsPage = () => {
    const [rewards, setRewards] = useState([]);
    const [rewardsPoints, setRewardsPoints] = useState('');
    const [rewardsMemberSince, setRewardsMemberSince] = useState('');
    const [customerID, setCustomerID] = useState('');
    const [editRewardsPoints, setEditRewardsPoints] = useState('');
    const [editRewardsMemberSince, setEditRewardsMemberSince] = useState('');
    const [editCustomerID, setEditCustomerID] = useState('');
    const [editRewardID, setEditRewardID] = useState('');
    

    const loadRewards = async () => {
        console.log('getting rewards from db');
        const response = await fetch('/rewards');
        const rewards = await response.json();
        setRewards(rewards);
    }

    const onAdd = async () => {
        // check for required fields
        if (!rewardsPoints) {
            alert('RewardsPoints is required to create a new reward.');
            return;
        }

        const newReward = {
            'rewardsPoints': rewardsPoints,
            'rewardsMemberSince' : rewardsMemberSince,
            'customerID': customerID,
        }
        const response = await fetch(`/rewards/`, {
            method: 'POST',
            body: JSON.stringify(newReward),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        const newRewardID = result[0]['customerID'];
        
        if (response.status === 201) {
            alert("Successfully added new reward!");
            newReward['customerID'] = newRewardID;
            let newRewards = rewards;
            newRewards.push(newReward);
            setRewards(newRewards);
            
            // reset values
            setRewardsPoints('');
            setCustomerID('');
        } else {
            console.error(`Failed to add reward, status code = ${response.status}`);
        };
    }

    const onDelete = async (customerID) => {
        const response = await fetch(`/rewards/${customerID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 204) {
            alert("Successfully deleted the reward!");
            const newRewards = rewards.filter(e => e.customerID !== customerID);
            setRewards(newRewards);
        } else {
            console.error(`Failed to delete reward with id = ${customerID}, status code = ${response.status}`);
        };
    }

    const onEdit = async (reward, i) => {
        setEditRewardsPoints(reward.rewardsPoints);
        setEditRewardsMemberSince(reward.rewardsMemberSince);
        setEditCustomerID(reward.customerID);
        setEditRewardID(reward.customerID);
    };

    const onSave = async () => {
        // check for required fields
        if (!editRewardsPoints) {
            alert('RewardsPoints cannot be blank.');
            return;
        }
        const updatedReward = {
            'rewardsPoints': editRewardsPoints,
            'customerID': editCustomerID,
        }
        const response = await fetch(`/rewards/${editRewardID}`, {
            method: 'PUT',
            body: JSON.stringify(updatedReward),
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 200) {
            alert("Successfully updated reward!");
            updatedReward['customerID'] = editRewardID;
            console.log(updatedReward, updatedReward.customerID);
            const updatedRewards = [];
            console.log(rewards);
            for (const reward of rewards) {
                console.log(reward);
                if (reward.customerID === updatedReward.customerID) {
                    updatedRewards.push(updatedReward);
                } else {
                    updatedRewards.push(reward);
                }
            }
            console.log(updatedRewards);
            setRewards(updatedRewards);
            
            // reset values
            setEditRewardsPoints('');
            setEditRewardsMemberSince('');
            setEditCustomerID('');
            setEditRewardID('');
        } else {
            console.error(`Failed to add reward, status code = ${response.status}`);
        };
    };

    useEffect(() => {
        loadRewards();
    }, []);

    return (
        <>
            <h1>Rewards</h1>
            <Navigation />
            <table classRewardsPoints="data-table" id="rewards-table">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>Reward ID</th>
                    <th>Rewards Points</th>
                    <th>Rewards Member Since</th>
                    <th>Customer ID</th>
                </tr>
            </thead>
            <tbody>
                {rewards.map((reward, i) => 
                <tr>
                    <td><button onClick={() => onEdit(reward, i)}>< BiEditAlt /></button></td>
                    <td><button onClick={() => onDelete(reward.customerID)}>< BiTrash /></button></td>
                    <td>{reward.rewardsPoints}</td>
                    <td>{reward.rewardsMemberSince}</td>
                    <td>{reward.customerID}</td>
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
                <legend><strong>Add Reward</strong></legend>
                    <fieldset>
                        <label> Rewards Points: </label> 
                            <input type="text" placeholder="" value={rewardsPoints} onChange={e => setRewardsPoints(e.target.value)} />
                        <label> Rewards Member Since: </label>
                            <input type="text" placeholder="" value={rewardsMemberSince} onChange={e => setRewardsMemberSince(e.target.value)} />
                        <label> Customer ID: </label> 
                            <input type="text" placeholder="" value={customerID} onChange={e => setCustomerID(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onAdd} >Add</button>
            </div>

            <div>
                <legend><strong>Update Reward</strong></legend>
                    <fieldset>
                        <input hidden type="text" value={editRewardID} />
                        <label> Rewards Points: </label> 
                            <input type="text" placeholder="" value={editRewardsPoints} onChange={e => setEditRewardsPoints(e.target.value)} />
                        <label> Rewards Member Since: </label>
                            <input type="text" placeholder="" value={editRewardsMemberSince} onChange={e => setEditRewardsMemberSince(e.target.value)} />
                        <label> Customer ID: </label> 
                            <input type="text" placeholder="" value={editCustomerID} onChange={e => setEditCustomerID(e.target.value)} />
                        <p></p>
                    </fieldset>
                <button onClick={onSave} >Save</button>
            </div>
        </>
    );
}

export default RewardsPage;