import {Component} from 'react';


class SensorAnalytics extends Component{
    constructor(props){
        super(props);
        this.state = {
            device_name: this.props.device_name
        }
    }
    render(){
        return(
            <div className="SensorAnalytics"></div>
        )
    }
}