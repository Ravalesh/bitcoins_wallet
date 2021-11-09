import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Redirect, useHistory } from "react-router";
import { getCustomerProfile, logoutUser } from "../service";
import * as actionTypes from "../store/actions";
import './HomePage.css'

const HomePage = () => {
  const dispatch = useDispatch();
  const userLoggedIn = useSelector((state) => state.userLoggedIn);
  const user = useSelector((state) => state.user);

  const history = useHistory();

  useEffect(() => {
    if (userLoggedIn) {
      const loginUser = async () => {
        console.log("getting customer profile..User ID: ", user.id);
        var apiResponse = await getCustomerProfile(user.id);
        if (apiResponse != null) {
          dispatch({
            type: actionTypes.UserProfile,
            user: {
              customerId:apiResponse.data.id,
              firstName: apiResponse.data.first_name,
              lastName: apiResponse.data.last_name,
              bitcoinBalance: apiResponse.data.bitcoin_balance,
            },
          });
        }
      };
      loginUser();
    }
  }, []);

  if (!userLoggedIn) {
    return <Redirect to="/login" />;
  }

  return (
    <div className="HomePage">
      {user && <h1>Hello {user.firstName}!</h1>}
      <div>
        {user && <h1>Your bitcoin balance is: {user.bitcoinBalance}!</h1>}
      </div>
      <div>
        <button
          type="button"
          onClick={() => {
            history.push("/sendbitcoins");
          }}
        >
          Send Bitcoins
        </button>
      </div>
      <div>
        <button
          type="button"
          onClick={async () => {
            var apiResponse = await logoutUser();
            if(apiResponse != null)
            dispatch({
                type: actionTypes.LogoutUser
              });
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default HomePage;
