import React, { Component } from 'react';
import Button from 'react-bootstrap/Button'
import ReactJson from 'react-json-view'
import './HarvestUnit.css'

class HarvestingUnit extends Component {
    constructor(props) {
        super(props)
        this.state = {
            collectionStatus: false
        }
        this.json = {"threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e", "doNotTrack": 1, "screenSize": "1920:1080", "plugins": ["Adblocks", "Google"], "position": {"lat": 95, "lng": 1.234525}, "browser": {"appName": "Netscape", "major": "67", "name": "Firefox", "version": "67.0"}, "cpu": {"architecture": "amd64"}, "os": {"name": "Windows", "version": "10"}}
    }

    onLaunchButtonClicked = () => {
        // TODO : START HARVESTING
        this.setState({
            collectionStatus: true
        })
    }

    onSendButtonClicked = () => {

    }

    render() {
        return (
            <div className="HarvestUnitContainer">
                {this.state.collectionStatus ? (
                    <div className="JsonContainer">
                        <h3>You will send these data :</h3>
                        <div className="JsonBox">
                            <ReactJson src={this.json} />
                        </div>
                        <Button 
                            variant="primary"
                            onClick={this.onSendButtonClicked}>
                            Envoyer
                        </Button>
                    </div>
                ) : (
                    <Button 
                        variant="outline-danger" 
                        size="lg"
                        onClick={this.onLaunchButtonClicked}>
                        Launch Data Collection
                    </Button>
                )}
            </div>
        )
    }
}

export default HarvestingUnit