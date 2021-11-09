import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {} from 'redux';
import { authenticate } from '../service';
import * as actionTypes from '../store/actions';
import './LoginComponent.css';

const LoginComponent = (props) =>{
    const dispatch = useDispatch();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const performLogin = async () =>{
        var apiResponse = await authenticate(
            username,
            password
          );
        if(apiResponse != null){
            console.log("Logged in! apiResponde: ", apiResponse);
            dispatch({type: actionTypes.LoginUser,
                        user:{
                            id:apiResponse.data.id
                        }
                        })
        }else{
            console.log("Login failed!");
        }

    };

    return(
        <section className="LoginComponent">
            <h1>Login</h1>
            <form onSubmit={performLogin}>
                <div>
                    <label htmlFor='username'  className="Textbox">Username</label>
                    <input value={username} id='username' onChange={(e) => 
                        {setUsername(e.target.value)}} required/>
                </div>
                <div>
                    <label htmlFor='password' className="Textbox">Password</label>
                    <input id='password' required value={password} onChange={(e) => 
                        {setPassword(e.target.value)}} type="password" />
                </div>
                <div>
                    <button type='button' onClick={performLogin}>
                        Login
                    </button>
                </div>
            </form>
        </section>
    );
};



export default  LoginComponent;