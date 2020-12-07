import {Component} from 'react'
import Fade from 'react-reveal/Fade'
import Typing from 'react-typing-animation';

class MainPage extends Component{ 
    constructor(props){
        super(props);
        this.state = {
            currWord:0,
        }
        this.randWords = ['Code', 'Create', 'Monke🐒', 'IoT', 'Think!', 'Coffee☕', 'JS', 'Evan🐵', 'Maged😫', 'Ousama🤑']
    }

    updateCurrWord = () =>{
        console.log(this.state.currWord)
        if(this.state.currWord === this.randWords.length){
            this.setState({currWord: 0});
        }else{
            this.setState({currWord: this.state.curr_word+=1});
        }
    }

    getRandWord = () => {
        return(
            <Typing loop={true} onFinishedTyping={this.updateCurrWord} hideCursor={true} className="LargeTitle">
                {this.randWords[this.state.currWord]}
                <Typing.Delay ms={1500} />
                <Typing.Backspace count={20} />
            </Typing>
    );
    }

    render(){
    return(
        <div className="MainPage">
            <h1 className="MainTitleContainer" style={{display:'flex'}}>
                <h1 className="LargeTitle">IO Space</h1>
                
            </h1>

            <div className="AboutIOSpace">
                <Fade>
                <h1 className="AboutHeader">What is IO Space?</h1>
                <p>IO Space is a highly interactive, easy to use IoT platform.IO Space can be easily used from any remote devices:cellphones, Lpatops ,Pcs and exatra</p>
                </Fade>
            </div>
            <div className="Getting Started">
                <Fade>
                <h1 className="AboutHeader">What is IO Space?</h1>
                <p>IO Space is a highly interactive, easy to use IoT platform. ADD MORE SHIT HERE, TOO TIRED</p>
                </Fade>
            </div>
            <div className="IOSpaceConnect" style={{display:'flex'}}>
                <Fade>
                <div className="InfoContainer">
                    <h1 className="InfoHeader">Existing User?</h1>
                    <p>
                        Existing users can log in using their unique API key, hit the button below to go to your sensors.
                        Loging in will bring you to MyIOSpace, where all your sensors and analytics are available at the
                        click of a button!
                    </p>
                    <button className="Button" onClick={() => {this.props.history.push("/login")}}>Login</button>
                </div>
                
                <div className="InfoContainer">
                    <h1 className="InfoHeader">New User?</h1>
                    <p>
                        Never been here before? Creating a new user is as easy as providing an email! Click the button below
                        to create your new API key. Keep a copy of this key at all times as it will allow you to setup your 
                        nodes and visualize data here!
                    </p>
                    <button className="Button" onClick={() => {this.props.history.push("/newUser")}}>Create!</button>
                </div>
                </Fade> 
            </div>
        </div>
    )
    }
}




export default MainPage;
