import React, {Component} from 'react'; 
import './DevicePageStyles.css'

class DevicePage extends Component{
    constructor(props){
        super(props);
        this.state = {
            device_name: props.device_name,
            device_type: "feedback",
            device_curr_val: ""
        }
    }
    render(){
        return(
            <div className="DevicePage">
                <div className="DevicePageHeader" style={{display:'flex'}}>
                    <div className="DeviceName">{this.state.device_name}</div>
                    <div className="DeviceType">{this.state.device_type}</div>
                    <img className="GitHubLogo" src="/github.png"></img>
                </div>
            </div>
        )
    }

}

export default DevicePage;