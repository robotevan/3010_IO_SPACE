import React from 'react'
import Fade from 'react-reveal/Fade'


export const MainPage = props => {
    return(
        <div className="MainPage">
            <h1 className="MainTitleContainer" style={{display:'flex'}}>
                <h1 className="LargeTitle">IO Space</h1>
                <h1 className="TypingText LargeTitle"></h1>
                <h1 className="Cursor LargeTitle">_</h1>
            </h1>

            <div className="AboutIOSpace">
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
                    <button className="Button" onClick={() => {props.history.push("/login")}}>Login</button>
                </div>
                
                <div className="InfoContainer">
                    <h1 className="InfoHeader">New User?</h1>
                    <p>
                        Never been here before? Creating a new user is as easy as providing an email! Click the button below
                        to create your new API key. Keep a copy of this key at all times as it will allow you to setup your 
                        nodes and visualize data here!
                    </p>
                    <button className="Button" onClick={() => {props.history.push("/newUser")}}>Create!</button>
                </div>
                </Fade> 
            </div>
        </div>
    )
}




export default MainPage;