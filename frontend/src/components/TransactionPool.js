import React,{useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import Transaction from './Transaction'
import {Button} from 'react-bootstrap'
import history from '../history'
import {API_BASE_URL, SECONDS_JS} from '../config'

const POLL_INTERVAL = 10*SECONDS_JS

function TransactionPool(){
    const [transactions, setTransaction] = useState([])

    const fetchTransactions = () => {
        fetch(`${API_BASE_URL}/transactions`)
            .then(response => response.json())
            .then(json => {
                console.log('transactions json',json)
                setTransaction(json)
            })
    }


    useEffect(() => {
        fetchTransactions()
        const intervalId = setInterval(fetchTransactions, POLL_INTERVAL);

        return () =>  clearInterval(intervalId)
    },[] )

    const fetchMineBlock = () => {
        fetch(`${API_BASE_URL}/blockchain/mine`)
            .then(() => {
                alert("SUCCESS!")
                history.push('/blockchain')
            })
    }


    return (
        <div className="TransactionPool">
            <Link to="/">Home</Link>
            <hr/>
            <h3>Transaction pool</h3>
            <div>
                {
                    transactions.map(transaction =>(
                        <div key={transaction.id}>
                            <hr/>
                            <Transaction transaction = {transaction}/>
                        </div>
                    ))
                }
            </div>
            <hr/>
            <Button variant="danger" onClick={fetchMineBlock}>
                Mine a block of these transactions
            </Button>
        </div>
    )
}

export default TransactionPool