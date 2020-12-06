import {Component} from 'react';

class NewUser extends Component{
    constructor(props){
        super(props);
        this.state = {
            "email":""
        }
        this.handleChange = this.handleChange.bind(this);
        this.createUserApiKey = this.createUserApiKey.bind(this);
    }


    handleChange(event) {
        this.setState({email: event.target.value});
    }

    createUserApiKey = () =>{
        fetch("/newUser/user?email="+ this.state.email).then(res => res.json()).then(data => {
            if (data["success"] == false){
                window.alert("The email you have entered is already registered!");
            }
        })
    }

    render(){
        return (
            <div className="Container">
            <div className="ConnectPage">
                <form onSubmit={this.createUserApiKey}>
                    <label>
                    Enter your email:
                    <input className="ConnectInput" type="email" value={this.state.api_key} onChange={this.handleChange} />
                    </label>
                    <input className="ConnectButton" type="submit" value="Create API Key" />
                </form>
            </div>
            </div>
        )
    }
}

export default NewUser;