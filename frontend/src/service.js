import config from './backendconfig.json'
import axios from 'axios';

let API_SERVER_VAL = '';

switch (process.env.NODE_ENV) {
    case 'development':
        API_SERVER_VAL = 'http://127.0.0.1:89';
        break;
    case 'production':
        API_SERVER_VAL = process.env.REACT_APP_API_SERVER;
        break;
    default:
        API_SERVER_VAL = 'http://127.0.0.1:89';
        break;
}

export async function authenticate(username, password){
    try{
        const axiosConfig = {
            headers: {"Content-Type":"application/json" }
        };
    
        const body = {
            "username": username,
            "password": password
        };
    
        var res = await axios.post(`${API_SERVER_VAL}${config.endpoints.authenticate}`,body, axiosConfig);
    
        if(res!=null && res.data != null && res.data.id != null){
            return res;
        }else{
            return null;
        }
    }catch (error) {
         console.log("Error",error);
         return null;
    }
}

export async function logoutUser(){
    try{
        var res = await axios.post(`${API_SERVER_VAL}${config.endpoints.logout}`, {withCredentials: true});
    
        if(res!=null && res.data != null && res.data.id != null){
            return true;
        }else{
            return false;
        }
    }catch (error) {
         console.log("Error",error);
         return false;
    }
}

export async function getCustomerProfile(customerId){
    try{

        const axiosConfig = {
            headers: {"Content-Type":"application/json" }
        };

        var res = await axios.get(`${API_SERVER_VAL}${config.endpoints.profile}?id=${customerId}`, axiosConfig);
        console.log("Customer profile received",res);
        if(res!=null && res.data != null && res.data.id != null){
            return res;
        }else{
            return null;
        }
    }catch (error) {
         console.log("Error",error);
         return null;
    }
}

export async function sendBitcoins(fromCustomerId, toAddress, amount){
    try{

        const axiosConfig = {
            headers: {"Content-Type":"application/json" }
        };

        const body = {
            "from_customer_id": fromCustomerId,
            "to_address": toAddress,
            "amount": amount
        };

        var res = await axios.post(`${API_SERVER_VAL}${config.endpoints.sendbitcoins}`,body, axiosConfig);
    
        if(res!=null && res.data != null && res.data.status != null){
            return res;
        }else{
            return null;
        }
    }catch (error) {
         console.log("Error",error);
         return null;
    }
}