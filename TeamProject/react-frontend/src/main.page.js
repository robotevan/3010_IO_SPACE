import React from 'react'

export const MainPage = props => {
    return(
        <div className="MainPage">
            <h1 className="MainTitleContainer" style={{display:'flex'}}>
                <h1 className="LargeTitle">IO Space</h1>
                <h1 className="TypingText LargeTitle"></h1>
                <h1 className="Cursor LargeTitle">_</h1>
            </h1>

            <div className="AboutIOSpace">
                <h1>What is IO Space?</h1>
                <p>IO Space is a highly interactive, easy to use IoT platform. ADD MORE SHIT HERE, TOO TIRED</p>
            </div>
            <div className="IOSpaceConnect" style={{display:'flex'}}>
                <div className="infoContainer">
                    <h1 className="InfoHeader">Existing User?</h1>
                    <button onClick={() => {props.history.push("/login")}}>Login</button>
                </div>
                <div className="infoContainer">
                    <h1 className="InfoHeader">New User?</h1>
                    <button onClick={() => {props.history.push("/newUser")}}>Create!</button>
                </div>
            </div>
        </div>
    )
}




export default MainPage;