import React, { Component } from 'react';
import './MainContainer.css';
import Navbar from 'react-bootstrap/Navbar'
import Presentation from './Presentation'
import HarvestingUnit from './HarvestingUnit'

class MainContainer extends Component {

    render() {
        return (
            <div className="MainContainer">
                <Navbar bg="light" variant="light">
                    <Navbar.Brand href="#home">
                        <img
                            alt=""
                            src="./brain.png"
                            className="d-inline-block"
                        />
                        <span>Project & Dissertation</span>
                    </Navbar.Brand>
                </Navbar>
                    <div className="PageTitle">
                        <h2>Machine Learning for Risk Assessment in Online Payment</h2>
                        <h4>Data Collection</h4>
                    </div>
                    <Presentation></Presentation>
                    <HarvestingUnit></HarvestingUnit>
            </div>
        )
    }
}

export default MainContainer