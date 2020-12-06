import React from 'react'
import ReactDom from 'react-dom';
import MainPage from './main.page';
import LoginPage from "./login.page";
import MyIOSpace from './MyIOSpace.page';
import {BrowserRouter, Route} from 'react-router-dom';

function App(){
    return(
        <div>
            <Route exact path="/" component={MainPage} />
            <Route exact path="/login" component={LoginPage} />
            <Route exact path="/MyIOSpace" component={MyIOSpace}/>
        </div>
    )
}

const rootElement = document.getElementById("root");
ReactDom.render(<BrowserRouter><App/></BrowserRouter>, rootElement);