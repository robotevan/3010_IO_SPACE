import { Component } from 'react';


class FeedbackState extends Component{
    state = {
        selectedDevice: 'none'
    }

    render(){
        return(
            <div className="CardContainer" style={{display:'flex'}}>
                <h1 className="CardText">test</h1>
            </div>
        )
    }
}

export default FeedbackState;