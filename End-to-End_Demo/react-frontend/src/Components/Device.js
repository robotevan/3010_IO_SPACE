import React, {Component} from 'react'; 
import '../Styles.css'

class Device extends Component{
    constructor(props){
        super(props)
        this.nodeId = props.deviceData.nodeId;
        this.deviceId = props.deviceData.deviceId;
        this.deviceName = props.deviceData.deviceName;
        this.deviceType = props.deviceData.deviceType;
        console.log(this.deviceName)
    }
    render(){
        return(
            <div className="Device">
                <div className="DeviceTitleContainer" style={{'display': 'flex'}}>
                    <div className="DeviceIdContainer TitleRoundContainer">Node {this.nodeId}</div>
                    <div className="DeviceTypeContainer TitleRoundContainer">{this.deviceType}</div>
                    <div className="DeviceNameContainer TitleRoundContainer">{this.deviceName}</div>
                </div>
                <div className="DeviceTitle">Current Data: {this.props.deviceData.deviceId}</div>
            </div>
        )
    }
}

export default Device;