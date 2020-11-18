import React, {useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import {FormGroup, FormControl, Button} from 'react-bootstrap'
import {API_BASE_URL} from '../config'
import history from '../history'

function ConductTransactions(){
    const [amount, setAmount] = useState(0)
    const [recepient, setRecepient] = useState('')
    const [knownAddresses, setKnownAddresses] = useState([])

    useEffect(() => {
        fetch(`${API_BASE_URL}/known/addresses`)
            .then(response => response.json())
            .then(json => setKnownAddresses(json))
    },[])

    const updateRecepient = event => {
       setRecepient(event.target.value)
    }

    const updateAmount = event => {
        setAmount(Number(event.target.value))
    }

    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`,{
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body :JSON.stringify({recepient, amount})
        }).then(response => response.json())
            .then(json => {
                console.log('submitTransaction json',json)
                alert("SUCCESS!")
                history.push('/transaction-pool')
            } )
    }

    return(
        <div className='ConductTransaction' >
            <Link to="/">Home</Link>
            <hr/>
            <h3>
                Conduct a transaction
            </h3>
            <br/>
            <FormGroup>
                <FormControl
                    input = "text"
                    placeholder = "recepient"
                    value = {recepient}
                    onChange = {updateRecepient}
                />
            </FormGroup>
            <FormGroup>
                <FormControl
                    input = "number"
                    placeholder = "amount"
                    value = {amount}
                    onChange = {updateAmount}
                />
            </FormGroup>
            <div>
                <Button
                    variant="danger"
                    onClick = {submitTransaction}
                >
                    Submit
                </Button>
            </div>
            <br/>
            <h4>
                Known addresses
            </h4>
            <div>
                {
                    knownAddresses.map((knownAddress,i) =>(
                        <span key={knownAddress}>
                            <u>{knownAddress}</u>
                            {i !== knownAddresses.length - 1 ? ', ' : ''}
                        </span>
                    ))
                }
            </div>

        </div>
    )

}

export default ConductTransactions