import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './components/App';
import {Router, Switch, Route} from 'react-router-dom'
import history from './history'
import Blockchain from './components/Blockchain'
import ConductTransactions from './components/ConductTransactions'
import TransactionPool from './components/TransactionPool'

ReactDOM.render(
  <Router history={history}>
    <Switch>
      <Route path='/' exact component={App}/>
      <Route path='/blockchain' component={Blockchain}/>
      <Route path='/conduct-transaction' component={ConductTransactions}/>
      <Route path='/transaction-pool' component={TransactionPool}/>
    </Switch>
  </Router>,
  document.getElementById('root')
);


