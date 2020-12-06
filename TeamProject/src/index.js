import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {login_page} from './login_page'
import {BrowserRouter, Route, Switch} from 'react-router-dom';


function App(){
  return (
    <div>
      <h1>Protected React Router</h1>
      <Route exact path="/" component={login_page}/>
    </div>
  )
}


//ReactDOM.render(
//  <React.StrictMode>
//    <App />
//  </React.StrictMode>,
//  document.getElementById('root')
//);