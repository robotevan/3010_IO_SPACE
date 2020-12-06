import {Component} from 'react';
import DeviceBar from './Components/DeviceBar'


class MyIOSpace extends Component{
    constructor(props){
        super(props);
        this.state = {
            selected_device:{
                nodeId:'',
                deviceName:'',
                deviceType: ''
            }
        }
    }

    setSelectedDevice = (nodeID, deviceName, deviceType) =>{
        console.log("device set to: " + deviceName);
        this.setState({selected_device: {
            nodeId: nodeID,
            deviceName:deviceName,
            deviceType: deviceType
        }});
    }

    render(){
        return(
            <div>
                <DeviceBar setDeviceFunc={this.setSelectedDevice}/>
            </div>
        )
    }
}

export default MyIOSpace;