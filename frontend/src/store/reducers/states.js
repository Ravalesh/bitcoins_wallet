import * as actionTypes from '../actions';

const initialState = {
    userLoggedIn:false,
    user:{
        id:0,
        customerId:0,
        firstName:'',
        lastName:'',
        bitcoinBalance:0
    }
};

const reducer = (state = initialState, action) => {
    if(action.type === actionTypes.LoginUser){
        return {
            ...state,
            userLoggedIn: true,
            user:{
                id: action.user.id
            }
        };
    }
    if(action.type === actionTypes.LogoutUser){
        return {
            ...state,
            userLoggedIn: false,
            user:{
                id:0,
                firstName:'',
                lastName:'',
                bitcoinBalance:0
            }
        };
    }
    if(action.type === actionTypes.UserProfile){
        return {
            ...state,
            user:{
                ...state.user,
                customerId:action.user.customerId,
                firstName:action.user.firstName,
                lastName:action.user.lastName,
                bitcoinBalance:action.user.bitcoinBalance
            }
        };
    }

    return state;
};

export default reducer;