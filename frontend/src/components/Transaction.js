import React from 'react'

function Transaction({transaction}) {
    const {input,output} = transaction
    const recepients = Object.keys(output)

    return (
        <div className='Transaction'>
            <div>From : {input.address}</div>
            {
                recepients.map(recepients =>(
                    <div key={recepients} >
                        To : {recepients} | Sent : {output[recepients]}
                    </div>
                ))
            }
        </div>
    )

}

export default Transaction