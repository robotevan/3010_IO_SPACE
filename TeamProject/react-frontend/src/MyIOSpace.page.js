import {Component} from 'react';
import DeviceBar from './Components/DeviceBar'


class MyIOSpace extends Component{
    constructor(props){
        super(props);
    }

    render(){
        return(
            <div>
                <DeviceBar />
            </div>
        )
    }
}

export default MyIOSpace;