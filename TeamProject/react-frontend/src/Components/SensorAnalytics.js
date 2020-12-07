import {Component} from 'react';
import '../../node_modules/react-vis/dist/style.css';
import {XYPlot, XAxis, YAxis, VerticalGridLines, HorizontalGridLines, LineSeries} from 'react-vis';

class SensorAnalytics extends Component{
    constructor(props){
        super(props);
        this.state = {
            deviceData: []
        }
        this.intervalId = 0;
        fetch(window.location.pathname + 
            "/sensorData" + window.location.search+
            "&node_name="+this.props.device[0]+
            "&device_name="+this.props.device[1]).then(res => res.json()).then(data => {
            this.setState({deviceData: data['deviceData']});
})
    }
    // When component is loaded start polling database every 10 seconds, checking if sensors updated
    async componentDidMount(){
        this.intervalId = setInterval(async () =>{
            fetch(window.location.pathname + 
                            "/sensorData" + window.location.search+
                            "&node_name="+this.props.device[0]+
                            "&device_name="+this.props.device[1]).then(res => res.json()).then(data => {
                this.setState({deviceData: data['deviceData']});
                console.log(this.state.deviceData);
              })
        }, 10000);
    }

    async componentWillUnmount(){
        clearInterval(this.intervalId);
    }

    render(){
        const nodeId = this.props.device[0];
        const deviceName = this.props.device[1];
        const deviceType = this.props.device[2];
        return(
            <div className="AnalyticsContainer">
                <h1 className="DeviceNameHeader">{deviceName}</h1>
                <div className="DataContainer" style={{display:'flex'}}>
                <div className="CardContainer" style={{display:'flex'}}>
                        <h1 className="CardText">Current State: </h1>
                    </div>
                <XYPlot height={400} width={600}>
                    <LineSeries data={this.state.deviceData}/>
                    <VerticalGridLines />
                    <HorizontalGridLines />
                    <XAxis />
                    <YAxis />
                </XYPlot>
                </div>
            </div>
        )
    }
}

export default SensorAnalytics;