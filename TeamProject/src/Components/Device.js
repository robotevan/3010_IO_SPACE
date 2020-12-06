import React, {Component} from 'react'; 
import '../Styles.css'

class Device extends Component{
    render(){
        const {nodeId, deviceName, deviceType, deviceCurrVal} = this.props.deviceData;
        return(
            <div className="Device">
                <div className="DeviceTitleContainer flex-container wrap" style={{'display': 'flex'}}>
                    <div className="DeviceIdContainer TitleRoundContainer">{nodeId}</div>
                    <div className="DeviceNameContainer TitleRoundContainer">{deviceName}</div>
                    <div className="DeviceTypeContainer TitleRoundContainer">{deviceType}</div>     
                </div>
                <div className="DeviceTitle">Current Data: {deviceCurrVal}</div>
            </div>
        )
    }
}

export default Device;