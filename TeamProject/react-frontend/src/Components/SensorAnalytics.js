import {Component} from 'react';


class SensorAnalytics extends Component{
    render(){
        return(
            <div className="SensorAnalytics">
                <h1 className="DeviceNameHeader">{this.props.device_name[1]}</h1>
            </div>
        )
    }
}

export default SensorAnalytics;