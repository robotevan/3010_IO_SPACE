import './Styles.css'
import DeviceBar from './Components/DeviceBar'
import DevicePage from './Components/DevicePage'

function App() {
    return(
      <div className="App">
        <DeviceBar key="test"/>
        <DevicePage device_name={"TEST"}/>
        
      </div>
    )
}

export default App;
