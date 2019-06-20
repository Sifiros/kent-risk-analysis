import React, { Component } from 'react';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import ReactJson from 'react-json-view'
import CircularProgress from '@material-ui/core/CircularProgress';
import HarvestedDataController from  '../Controllers/HarvestedDataController'
import getAllInfo from '../harvester'
import './HarvestUnit.css'
import PropTypes from 'prop-types';

let CollectionState = {
    IDLE: 0,
    COLLECTION: 1,
    COLLECTED: 2,
    SENT: 3
}

const understandingEn = "I confirm I have read and understand the information for the above study"
const understandingFr = "Je confirme avoir lu et compris les informations à propos cette étude"
const voluntaryEn = "I understand that my participation is voluntary and that I am free to withdraw at any time without giving any reason"
const voluntaryFr = "Je comprends que ma participation est volontaire et que je peux me retirer à tout moment sans donner de raison particulière"
const gdprEn = "I understand that my responses will be anonymised before analysis. I give permission for members of the research team to have access to my anonymised responses."
const gdprFr = "Je comprends que mes réponses seront anonymisées avant l'analyse. Je donne la permission aux membres de l'étude d'avoir accès à mes données anonymisées"
const dataCollectionButtonLabelEn = "Launch Data Collection"
const dataCollectionButtonLabelFr = "Lancer la collecte de données"
const sendDataButtonLabelEn = "Send"
const sendDataButtonLabelFr = "Envoyer"
const jsonBoxLabelEn = "You will send these data :"
const jsonBoxLabelFr = "Vous allez envoyer ces données :"
const thanksMessageEn = "Thanks for your contribution"
const thanksMessageFr = "Merci pour votre contribution"
const gatheringLabelEn = "Gathering data, loading..."
const gatheringLabelFr = "Récolte des données, chargement ..."

class HarvestingUnit extends Component {
    constructor(props) {
        super(props)
        this.state = {
            collectionState: CollectionState.IDLE,
            language: props.language,
            understanding: false,
            voluntary: false,
            gdpr: false,
            isNotAbleToSend: true
        }
        this.harvestedDataController = new HarvestedDataController()
    }

    componentWillReceiveProps(props) {
        this.setState({
            language: props.language
        })
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

    onUnderstandingCheckboxChanged = (value) => {
        this.setState({
            understanding: value.target.checked
        })
    }

    onVoluntaryCheckboxChanged = (value) => {
        this.setState({
            voluntary: value.target.checked
        })
    }

    onGdprCheckboxChanged = (value) => {
        this.setState({
            gdpr: value.target.checked
        })
    }

    render() {
        return (
            <div className="HarvestUnitContainer">
                {this.state.collectionState === CollectionState.COLLECTION ? (
                    <div className="LoadingOverlayBoxContainer">
                        <div className="LoadingOverlayBox">
                            <h2>{this.state.language === "fr" ? gatheringLabelFr : gatheringLabelEn}</h2>
                            <CircularProgress/>
                        </div>
                    </div>
                ) : this.state.collectionState === CollectionState.SENT ? (
                    <div className="ThanksContainer">
                        <div className="ThanksBox">
                            <h2>{this.state.language === "fr" ? thanksMessageFr : thanksMessageEn}</h2>
                        </div>
                    </div>
                ) : this.state.collectionState === CollectionState.COLLECTED ? (
                    <div className="JsonContainer">
                        <h3>{this.state.language === "fr" ? jsonBoxLabelFr : jsonBoxLabelEn}</h3>
                        <div className="JsonBox">
                            <ReactJson src={this.json} collapseStringsAfterLength={40}/>
                        </div>
                        <Button 
                            variant="primary"
                            onClick={this.onSendButtonClicked}>
                            {this.state.language === "fr" ? sendDataButtonLabelFr : sendDataButtonLabelEn}
                        </Button>
                    </div>
                ) : (
                    <div className="FormContainer">
                        <Form.Group controlId="UnderstandingCheckbox">
                            <Form.Check value={this.state.understanding} type="checkbox" label={this.state.language === "fr" ? understandingFr : understandingEn} onChange={this.onUnderstandingCheckboxChanged}/>
                            <Form.Check value={this.state.voluntary} type="checkbox" label={this.state.language === "fr" ? voluntaryFr : voluntaryEn} onChange={this.onVoluntaryCheckboxChanged}/>
                            <Form.Check value={this.state.gdpr} type="checkbox" label={this.state.language === "fr" ? gdprFr : gdprEn} onChange={this.onGdprCheckboxChanged}/>
                        </Form.Group>
                        <Button 
                            variant="outline-danger" 
                            size="lg"
                            disabled={!(this.state.voluntary === true && this.state.understanding === true && this.state.gdpr === true)}
                            onClick={this.onLaunchButtonClicked}>
                            {this.state.language === "fr" ? dataCollectionButtonLabelFr : dataCollectionButtonLabelEn}
                        </Button>
                    </div>
                )}
            </div>
        )
    }
}

HarvestingUnit.propTypes = {
    language: PropTypes.string
}
  
HarvestingUnit.defaultProps = {
    language: "fr"
}

export default HarvestingUnit