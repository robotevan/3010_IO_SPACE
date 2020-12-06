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
        fetch("/newUser/user?email="+ this.state.email)
    }

    render(){
        return (
            <div className="LoginPage">
                <form onSubmit={this.verifyLogin}>
                    <label>
                    Enter your email:
                    <input type="text" value={this.state.api_key} onChange={this.createUserApiKey} />
                    </label>
                    <input type="submit" value="Create API Key" />
                </form>
            </div>
        )
    }
}

export default NewUser;