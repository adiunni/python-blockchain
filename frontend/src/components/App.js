import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";
import { API_BASE_URL } from "../config";

function App() {
  const [walletInfo, setWalletInfo] = useState({});
  const [apiURL] = useState(localStorage.getItem("NetURL") || API_BASE_URL);

  useEffect(() => {
    fetch(`${apiURL}/wallet/info`)
      .then((response) => response.json())
      .then((json) => setWalletInfo(json));
  }, [apiURL]);

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <br />
      <img
        className="logo"
        src={logo}
        style={{
          width: "150px",
          height: "150px",
        }}
        alt="App Logo"
      />
      <h3>Welcome to ProtoCrit</h3>
      <br />
      <Link to="/blockchain">Blockchain</Link>
      <Link to="/conduct-transaction">Conduct transaction</Link>
      <Link to="/transaction-pool">Transaction pool</Link>
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
    </div>
  );
}

export default App;
