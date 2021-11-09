import logo from './logo.svg';
import './App.css';
import { Route, Switch } from 'react-router';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SendBitCoins from './pages/SendBitcoins';

function App() {
  return (
   <Switch>
     <Route path='/' exact>
       <HomePage />
     </Route>
     <Route path='/login' exact>
       <LoginPage />
     </Route>
     <Route path='/sendbitcoins' exact>
       <SendBitCoins />
     </Route>
   </Switch>
  );
}

export default App;
