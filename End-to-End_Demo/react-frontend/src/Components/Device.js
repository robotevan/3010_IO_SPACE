import React, {Component} from 'react'; 
import '../Styles.css'

class Device extends Component{
    constructor(props){
        super(props)
        this.state = {
            nodeId: props.deviceData.nodeId,
            deviceId: props.deviceData.deviceId,
            deviceName: props.deviceData.deviceName,
            deviceType: props.deviceData.deviceType,
            deviceVal: props.deviceData.deviceCurrVal,
            latestUpdate: props.deviceData.timeStamp
        }
    }
    
    render(){
        return(
            <div className="Device">
                <div className="DeviceTitleContainer flex-container wrap" style={{'display': 'flex'}}>
                    <div className="DeviceIdContainer TitleRoundContainer">{this.state.nodeId}</div>
                    <div className="DeviceNameContainer TitleRoundContainer">{this.state.deviceName}</div>
                    <div className="DeviceTypeContainer TitleRoundContainer">{this.state.deviceType}</div>     
                </div>
                <div className="DeviceTitle">Current Data: {this.state.deviceVal}</div>
            </div>
        )
    }
}

export default Device;