import React, {Component} from 'react'; 

class SensorDevicePage extends Component{
    constructor(props){
        super(props);
         this.state = {
             sensor_name,
             data: []
         }
    }

    /*
    async componentDidMount(){
        setInterval(async () =>{
            fetch(this.state.sensor_name).then(res => res.json()).then(data => {
                this.setState()
              })
        }, 10000);
    }
    */

    render(){
        return(
            <div>
                <div className="CurrSensorStatus" style={{'display':"flex"}}>
                    <div>Current Sensor Data: {this.state.data[0]}</div>
                </div>
            </div>

        )
    }

}