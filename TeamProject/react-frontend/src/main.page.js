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
                <p>IO Space is a highly interactive, easy to use IoT platform.IO Space can be easily used from any remote devices:cellphones, Lpatops ,Pcs and exatra</p>
                </Fade>
            </div>
            <div className="Getting Started">
                <Fade>
                <h1 className="AboutHeader">How to get started?</h1>
                <p>TO get started its 4 easy steps, 1. sign up,2.get youe api key,3.create a node, 4. use a sensor and your all done </p>
                </Fade>
            </div>
            <div className="Sign Up">
                <Fade>
                <h1 className="AboutHeader">How to sign up?</h1>
                <p>siging up is really easily, enter your email below to reicve your api key and you are reay to start  </p>
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
    <html>
   <head>
      <style>
         body {
            background-image: url("https://lh3.googleusercontent.com/YGJ77qN9KiwctZgfqV8Bf3hNo0rZvcFaPKDTkvtS6kVbtwyCS80Pm6dpXzJCCLZE1Q");
         }
      </style>
   </head>

   <body>
      <h1>Connect with Tutors</h1>
   </body>
</html>




    )
}




export default MainPage;
