import React, {Component} from 'react'; 
import '../Styles.css'
import Device from './Device'


class DeviceBar extends Component{
    state = {
        devices: []
    }
    constructor(){
        super()
        // Fetch initial list of sensors in the database
        fetch(window.location.pathname).then(res => res.json()).then(data => {
            this.setState({devices: data.devices});
          })
    }

    // When component is loaded start polling database every 10 seconds, checking if sensors updated
    async componentDidMount(){
        setInterval(async () =>{
            fetch(window.location.pathname).then(res => res.json()).then(data => {
                this.setState({devices: data.devices});
              })
        }, 10000);
    }

    render(){
        return(
            <div className="DeviceBar">
                <div className="DeviceBarHeader">My Devices: {this.state.devices.length}</div>
                <div className="DeviceList">
                    {
                        this.state.devices.map((device)=> (
                            <Device key={device.deviceID} deviceData={device}/>
                        ))                        
                    }
                </div>
            </div>
        )
    }
}

export default DeviceBar;