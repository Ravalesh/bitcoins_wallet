import { useSelector } from 'react-redux';
import LoginComponent from "../components/LoginComponent";
import { Redirect } from 'react-router';

const LoginPage = () =>{
    const userLoggedIn = useSelector(state => state.userLoggedIn);
    if(userLoggedIn){
        return <Redirect to="/" />;
    }
    return <LoginComponent />;
};

export default LoginPage