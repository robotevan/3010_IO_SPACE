import React from 'react'
import ReactDom from 'react-dom';
import MainPage from './main.page';
import LoginPage from "./login.page";
import NewUser from './newUser.page';
import MyIOSpace from './MyIOSpace.page';
import {BrowserRouter, Route} from 'react-router-dom';

import "./styles.css"

function App(){
    return(
        <div>
            <Route exact path="/" component={MainPage} />
            <Route exact path="/login" component={LoginPage} />
            <Route exact path="/newUser" component = {NewUser} />
            <Route exact path="/MyIOSpace" component={MyIOSpace}/>
        </div>
    )
}

const rootElement = document.getElementById("root");
ReactDom.render(<BrowserRouter><App/></BrowserRouter>, rootElement);