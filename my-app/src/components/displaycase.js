import React, { useEffect, useState } from "react";
import "./displaycase.css";
import { useRef } from 'react';
import axios from 'axios'
import { Audio } from 'react-loader-spinner'

const DisplayCase = (props) => {
  const [getMessage, setGetMessage] = useState({})


  useEffect(()=>{
    axios.get('http://localhost:5000/flask/hello').then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])

  if (props.loading === true){
    return (
      <div className="flex-container">
      <div className="sidebar">
      </div>
      <div className="showCase" id="loading-fam">
      <Audio
        height="80"
        width="80"
        radius="9"
        color="green"
        ariaLabel="loading"
        wrapperStyle
        wrapperClass
      />
      </div>
      </div>
    )
  }

  if (props.processedData.length === 0) {
    return (
    <div className="flex-container">
    <div className="sidebar">
                <ul className="sideList">
                <a href="#top" className="heading">GO TO TOP</a>
                <li className="heading">CONTENT</li>
                <a href="#thegood" className="sideItem">Positive Reviews</a>
                <a href="#thebad" className="sideItem">Negative Reviews</a>
                <a href="#theirrelevant" className="sideItem">Unrelated Reviews</a>
                </ul>
    </div>
    <div className="showCase" id="empty-fam">
      <div className="empty-message">
        <p>Please enter the name of your business and its postal code to get started...</p>
      </div>
    </div>
    </div>
    );
  }

    return (
        <div className="flex-container">
            <div className="sidebar">
                <ul className="sideList">
                <a href="#top" className="heading">GO TO TOP</a>
                <li className="heading">CONTENT</li>
                <a href="#thegood" className="sideItem">Positive Reviews</a>
                <a href="#thebad" className="sideItem">Negative Reviews</a>
                <a href="#theirrelevant" className="sideItem">Unrelated Reviews</a>
                </ul>
            </div>
            <div className="showCase">
                <div className="header" id="top">
                    <h1 style={{textTransform: "capitalize"}}>{props.processedData[5]}</h1>
                    <div className="divider"></div>
                </div>
                <div className="rating">
                    <div class="cut-rectangle"></div>
                    <div class="triangle"></div>
                    <div class="square"></div>
                </div>
                <div className="overallStats">
                    <p> Here's how <span style={{textTransform: "capitalize"}}>{props.processedData[5]}</span> performed at a glance:</p>
                    <div className="flexStats">
                        <p id="statOne">{props.processedData[0]}% Positive</p>
                        <p id="statTwo">{props.processedData[1]}%  Negative</p>
                        <p id="statThree">{props.processedData[2]}% Unrelated</p>
                    </div>
                </div>
                <div className="thegood" id="thegood">
                    <h2>Positive Reviews</h2>
                    <p>Here is what customers enjoyed most about your restaurant:</p>
                    <br/>
                    <p>{props.processedData[3]}</p>
                </div>
                <div className="thebad" id="thebad">
                    <h2>Negative Reviews</h2>
                    <p>Here is what customers disliked about your restaurant:</p>
                    <br/>
                    <p>{props.processedData[4]}</p>
                </div>
            </div>
        </div>
    )
}

export default DisplayCase