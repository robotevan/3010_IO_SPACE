import {Component} from 'react';


class FeedbackAnalytics extends Component{
    constructor(props){
        super(props);
        this.state = {
            deviceVal: 0,
        }
        
        // get the initital device value, cant change from client side so no point in polling
        fetch(window.location.pathname+window.location.search).then(res => res.json()).then(data => {
            this.setState({deviceVal: 1})
        })
        // bind functions
        this.deviceOn = this.deviceOn.bind(this);
        this.deviceOff = this.deviceOff.bind(this);
    }
    

    deviceOn = () =>{
        fetch(window.location.pathname + "/deviceOn" + 
                            window.location.search+
                            "&node_name="+this.props.device[0]+ // set device node name and device name
                            "&device_type="+this.props.device[1]).then(res => res.json()).then(data => {
            this.setState({deviceVal: 1});
        })
    }

    deviceOff = () =>{
        fetch(window.location.pathname + "/deviceOff" + 
                            window.location.search+
                            "&node_name="+this.props.device[0]+ // set device node name and device name
                            "&device_type="+this.props.device[1]).then(res => res.json()).then(data => {
            this.setState({deviceVal: 0});
        })
    }

    render(){
        const nodeId = this.props.device[0];
        const deviceName = this.props.device[1];
        const deviceType = this.props.device[2];
        return(
            <div className="AnalyticsContainer">
                <h1 className="DeviceNameHeader">{deviceName}</h1>
                <div className="StateContainer" style={{display:'flex'}}>
                    <div className="CardContainer" style={{display:'flex'}}>
                        <h1 className="CardText">Current State: </h1>
                        <h1 className="CardText">{this.state.deviceVal}</h1>
                    </div>
                    <button className="CardContainer" id="OnButton" onClick={this.deviceOn} style={{display:'flex'}}>
                        <h1 className="CardText"id="OnButton"> On </h1>
                    </button>
                    <button className="CardContainer" id="OffButton" onClick={this.deviceOff} style={{display:'flex'}}>
                        <h1 className="CardText" id="OffButton"> Off </h1>
                    </button>
                </div>
            </div>
        )
    }
}

export default FeedbackAnalytics;