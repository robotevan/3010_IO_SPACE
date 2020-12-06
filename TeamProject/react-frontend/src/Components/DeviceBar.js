import React, {Component} from 'react'; 
import Device from './Device';
import './componentSyles.css'


class DeviceBar extends Component{
    state = {devices: [],
            connected: false}


    get_devices_style = () =>{
        if (this.state.connected){
            return("My Devices: ")
        }else{
            return("Please enter a valid device name in the url api/<apikey>")
        }

    }

    update = (data)=>{
        if (data.devices === "NoneFound"){
            this.setState({devices: []})
            this.setState({connected: false})
        }else{
            this.setState({connected: true})
            this.setState({devices: data.devices});
        }
    }

    // When component is loaded start polling database every 10 seconds, checking if sensors updated
    async componentDidMount(){
        setInterval(async () =>{
            fetch(window.location.pathname+window.location.search).then(res => res.json()).then(data => {
                this.update(data);
              })
        }, 4000);
    }

    render(){
        return(
            <div className="DeviceBar">
                <div className="DeviceBarHeader">{this.get_devices_style()}{this.state.devices.length}</div>
                <div className="DeviceList">
                    {
                        this.state.devices.map((device)=> (
                            <Device key={device.deviceId} deviceData={device}/>
                        ))                        
                    }
                </div>
            </div>
        )
    }
}

export default DeviceBar;