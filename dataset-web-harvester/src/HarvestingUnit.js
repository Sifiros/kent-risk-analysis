import React, { Component } from 'react';
import Button from 'react-bootstrap/Button'
import ReactJson from 'react-json-view'
import './HarvestUnit.css'

let CollectionState = {
    IDLE: 0,
    COLLECTED: 1,
    SENT: 2
}

class HarvestingUnit extends Component {
    constructor(props) {
        super(props)
        this.state = {
            collectionState: CollectionState.IDLE
        }
        this.json = {"doNotTrack": 1, "screenSize": "1920:1080", "plugins": ["Adblocks", "Google"], "position": {"lat": 95, "lng": 1.234525}, "browser": {"appName": "Netscape", "major": "67", "name": "Firefox", "version": "67.0"}, "cpu": {"architecture": "amd64"}, "os": {"name": "Windows", "version": "10"}}
    }

    onLaunchButtonClicked = () => {
        // TODO : START HARVESTING
        this.setState({
            collectionState: CollectionState.COLLECTED
        })
    }

    onSendButtonClicked = () => {
        // TODO : PUSH DATA ON FIREBASE
        this.setState({
            collectionState: CollectionState.SENT
        })
    }

    render() {
        return (
            <div className="HarvestUnitContainer">
                {this.state.collectionState === CollectionState.COLLECTED ? (
                    <div className="JsonContainer">
                        <h3>You will send these data :</h3>
                        <div className="JsonBox">
                            <ReactJson src={this.json} />
                        </div>
                        <Button 
                            variant="primary"
                            onClick={this.onSendButtonClicked}>
                            Send
                        </Button>
                    </div>
                ) : this.state.collectionState === CollectionState.SENT ? (
                    <div className="ThanksContainer">
                        <div className="ThanksBox">
                            <h2>Thanks for your contribution</h2>
                        </div>
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