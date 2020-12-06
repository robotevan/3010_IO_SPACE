import React, {Component} from 'react'; 
import Device from './Device';
import '../styles.css'


class DeviceBar extends Component{
    constructor(props){
        super(props);
        fetch(window.location.pathname+window.location.search).then(res => res.json()).then(data => {
            this.update(data);
        })
    }
    state = {devices: []
        }
    intervalId = 0;


    get_devices_style = () =>{
        return("My Devices: ");
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
        this.state.intervalId = setInterval(async () =>{
            fetch(window.location.pathname+window.location.search).then(res => res.json()).then(data => {
                this.update(data);
              })
        }, 10000);
    }

    async componentWillUnmount(){
        clearInterval(this.state.intervalId);
    }

    render(){
        return(
            <div className="DeviceBar">
                <div className="DeviceBarHeader">{this.get_devices_style()}{this.state.devices.length}</div>
                <div className="DeviceList">
                    {
                        this.state.devices.map((device)=> (
                            <Device key={device.deviceId} deviceData={device} setDeviceFunc={this.props.setDeviceFunc}/>
                        ))                        
                    }
                </div>
            </div>
        )
    }
}

export default DeviceBar;