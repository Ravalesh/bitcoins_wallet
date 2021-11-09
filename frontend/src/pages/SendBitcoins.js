import { Link } from "react-router-dom";
import { sendBitcoins } from "../service";
import { useSelector } from "react-redux";
import { useState } from "react";
import './SendBitcoins.css'

const SendBitCoins = () => {
  const user = useSelector((state) => state.user);

  const [address, setAddress] = useState("");
  const [amount, setAmount] = useState(0.0);

  const [bitcoinsSent, setBitcoinsSent] = useState(false);
  const [error, setError] = useState("");

  const handleSend = async () => {
    console.log("user ID is", user.id)
    var apiResponse = await sendBitcoins(user.customerId, address, amount);
    if (apiResponse != null) {
      setBitcoinsSent(true);
      setError("");
    }else{
        setError("Error sending bitcoins!");
    }
  };

  return (
    <div className="SendBitcoins">
      <h1>Send Bitcoins</h1>
      {!bitcoinsSent ? (
        <div>
          <div>
            <label htmlFor="address" className="SendBitcoinsTextbox">Address</label>
            <input
              value={address}
              onChange={(e) => {
                setAddress(e.target.value);
              }}
              type="text"
              id="address"
            />
          </div>
          <div>
            <label htmlFor="bitcoins" className="SendBitcoinsTextbox">Bitcoins</label>
            <input
              value={amount}
              type="number"
              id="bitcoins"
              onChange={(e) => {
                setAmount(e.target.value);
              }}
            />
          </div>
          <div>
            <button type="button" onClick = {handleSend}>Send</button>
          </div>
        </div>
      ) : (
        <div> <h3>{amount} Bitcoins successfully sent to {address}</h3></div>
      )}

      {
          error && error !== ""?
          (
              <div> {error} </div>
          ):
          (<div> </div>)
      }

      <Link to="/">Home</Link>
    </div>
  );
};

export default SendBitCoins;
