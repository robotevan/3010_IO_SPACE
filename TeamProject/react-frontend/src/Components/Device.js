import React, {Component} from 'react'; 
import './componentSyles.css'

class Device extends Component{
    constructor(props){
        super(props);
        this.setDeviceFunc = this.setDeviceFunc.bind(this);
    }
    
    setDeviceFunc = (node, device, type) =>{
        this.props.setDeviceFunc(node, device, type);
    }
    

    render(){
        const {nodeId, deviceName, deviceType, deviceCurrVal} = this.props.deviceData;
        return(
            <div className="Device" onClick={e => this.setDeviceFunc(nodeId, deviceName, deviceType)}>
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