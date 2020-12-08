import {Component} from 'react';

class LoginPage extends Component{
    constructor(props){
        super(props);
        this.state = {
            "api_key":""
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    handleChange(event) {
        this.setState({api_key: event.target.value});
    }

    handleSubmit(event) { // function to call when button clicked
        this.verifyLogin(this.state.api_key);
        event.preventDefault();
    }

    verifyLogin = (api_key) =>{
        fetch("/login/user?api_key="+api_key).then(res => res.json()).then(data =>{
            if(data["valid_user"] == true){ // valid api key, proceed to application
                console.log("logging in");
                this.props.history.push("/MyIOSpace?api_key="+api_key); // go to my io space with provided api key
            } else{  // Invalid api key, alert user
                window.alert("The API key you entered is invalid, please try again")
            }
        })
    }

    render(){
        return (
            <div className="Container">
                <button className="CardContainer" id="backButton" onClick={() => {this.props.history.push("/")}} style={{display:'flex'}}>
                        <h1 className="CardText"> 🔙Back </h1>
                    </button>
            <div className="ConnectPage">
                <form onSubmit={this.handleSubmit}>
                    <label>
                    Enter Your API Key:
                    <input className="ConnectInput" type="text" value={this.state.api_key} onChange={this.handleChange} />
                    </label>
                    <input className="ConnectButton" type="submit" value="Connect" />
                </form>
            </div>
            </div>
        )
    }
}

export default LoginPage;