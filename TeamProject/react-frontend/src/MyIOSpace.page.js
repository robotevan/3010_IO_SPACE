import {Component} from 'react';
import DeviceBar from './Components/DeviceBar'
import SensorAnalytics from './Components/SensorAnalytics'

class MyIOSpace extends Component{
    constructor(props){
        super(props);
        this.state = {
            selected_device:[]
        }
    }

    setSelectedDevice = (nodeID, deviceName, deviceType) =>{
        console.log("device set to: " + deviceName);
        this.setState({selected_device: [nodeID, deviceName, deviceType]});
    }

    render(){
        return(
            <div>
                <DeviceBar setDeviceFunc={this.setSelectedDevice} />
                <SensorAnalytics device_name={this.state.selected_device} />
            </div>
        )
    }
}

export default MyIOSpace;