import {Component} from 'react';
import DeviceBar from './Components/DeviceBar'
import SensorAnalytics from './Components/SensorAnalytics'
import FeedbackAnalytics from './Components/FeedbackAnalytics'


class MyIOSpace extends Component{
    state = {
        selected_device: "none"
    }
    setSelectedDevice = (nodeID, deviceName, deviceType) =>{
        console.log("device set to: " + deviceName);
        this.setState({selected_device: [nodeID, deviceName, deviceType]});
    }


    getPage = () =>{
        if(this.state.selected_device[2] === "feedback"){
            return <FeedbackAnalytics device={this.state.selected_device} />
        }else if(this.state.selected_device[2] === "sensor"){
            return <SensorAnalytics device={this.state.selected_device} />
        }else{
            return;
        }
    }

    render(){
        return(
            <div>
                <DeviceBar setDeviceFunc={this.setSelectedDevice} />
                {this.getPage()}
            </div>
        )
    }
}

export default MyIOSpace;