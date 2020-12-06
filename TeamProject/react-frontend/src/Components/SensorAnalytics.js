import {Component} from 'react';


class SensorAnalytics extends Component{
    render(){
        const nodeId = this.props.device[0];
        const deviceName = this.props.device[1];
        const deviceType = this.props.device[2];
        return(
            <div className="AnalyticsContainer">
                <h1 className="DeviceNameHeader">{deviceName}</h1>
            </div>
        )
    }
}

export default SensorAnalytics;