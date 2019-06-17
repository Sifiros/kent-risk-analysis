import React, { Component } from 'react';
import Button from 'react-bootstrap/Button'
import ReactJson from 'react-json-view'
import CircularProgress from '@material-ui/core/CircularProgress';
import HarvestedDataController from  '../Controllers/HarvestedDataController'
import getAllInfo from '../harvester'
import './HarvestUnit.css'

let CollectionState = {
    IDLE: 0,
    COLLECTION: 1,
    COLLECTED: 2,
    SENT: 3
}

class HarvestingUnit extends Component {
    constructor(props) {
        super(props)
        this.state = {
            collectionState: CollectionState.IDLE
        }
        this.harvestedDataController = new HarvestedDataController()
    }

    onLaunchButtonClicked = () => {
        this.setState({
            collectionState: CollectionState.COLLECTION
        })
        getAllInfo().then(res => {
            console.log(res)
            // Replace potencial undefined fields by null to be able to post data to the db
            let replacer = (key, value) =>
                typeof value === 'undefined' ? null : value;
            let stringified = JSON.stringify(res, replacer)
            this.json = JSON.parse(stringified)

            this.setState({
                collectionState: CollectionState.COLLECTED
            })
        })
    }

    onSendButtonClicked = () => {
        this.harvestedDataController.createHarvestedData(this.json)
        this.setState({
            collectionState: CollectionState.SENT
        })
    }

    render() {
        return (
            <div className="HarvestUnitContainer">
                {this.state.collectionState === CollectionState.COLLECTION ? (
                    <div className="LoadingOverlayBoxContainer">
                        <div className="LoadingOverlayBox">
                            <h2>Gathering data, loading...</h2>
                            <CircularProgress/>
                        </div>
                    </div>
                ) : this.state.collectionState === CollectionState.SENT ? (
                    <div className="ThanksContainer">
                        <div className="ThanksBox">
                            <h2>Thanks for your contribution</h2>
                        </div>
                    </div>
                ) : this.state.collectionState === CollectionState.COLLECTED ? (
                    <div className="JsonContainer">
                        <h3>You will send these data :</h3>
                        <div className="JsonBox">
                            <ReactJson src={this.json} collapseStringsAfterLength={40}/>
                        </div>
                        <Button 
                            variant="primary"
                            onClick={this.onSendButtonClicked}>
                            Send
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