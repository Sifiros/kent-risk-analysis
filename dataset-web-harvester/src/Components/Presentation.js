import React, { Component } from 'react';
import './Presentation.css';
import { SegmentedControl } from 'segmented-control'
import MDReactComponent from 'markdown-react-js';
import PropTypes from 'prop-types';

let frenchPresentation = `Dans le cadre de notre 4ème année d’étude, nous devons réaliser un projet de recherche afin de valider notre Master.

Nous travaillons actuellement sur de l’analyse de risque lors d’une transaction en ligne en cherchant à vérifier l’identité de la personne réalisant l’achat.
A chaque paiement, des données de l’utilisateur qualifiant son navigateur et sa transaction seront utilisées pour créer un profil puis analysées par une intelligence artificielle 
qui permettra de qualifier s’il existe une corrélation entre le dernier relevé et le reste du profil de l’acheteur et donc de vérifier son identité.
Ce projet vise donc à rendre les paiements en lignes toujours plus sécurisés.
Afin de réaliser un entrainement préliminaire de notre intelligence artificielle, nous avons besoin de données variées et c’est pour cela que nous avons besoin de vous.

En pressant le bouton rouge au dessous de ce texte vous nous permettrez d’accéder exceptionnellement aux données suivantes :

* Votre système d’exploitation ainsi que sa version
* La marque et le modèle du matériel que vous utilisez ainsi que sa version
* Le navigateur web que vous utilisez ainsi que sa version
* Le logiciel moteur de rendu du navigateur que vous utilisez ainsi que sa version
* Les plug-ins (et non pas les extentions) actuellement installés sur votre navigateur (si autorisé par votre navigateur)
* L’état du mode “doNotTrack” de votre navigateur
* La taille actuelle de la fenêtre de votre navigateur
* La liste des différentes polices d’écriture installées sur votre navigateur
* La liste des différents encodages supportés par votre navigateur
* La liste des différentes langues installées sur votre navigateur
* Les différents formats de contenus supportés par votre navigateur
* L’architecture de votre processeur
* Votre fuseau horaire actuel
* Votre position actuelle approximative (si autorisée par votre navigateur) - *Optionnel*

Notez que l’ensemble de ces données ne permettent aucunement l’identification d’une personne et qu’elles seront **directement anonymisées** et **détruites
à la fin de l’étude** (début septembre 2019) afin d’être **complètement conforme à la loi  européene** (RGPD).
Une fois le bouton pressé, nous vous présenterons l’ensemble des données que vous allez nous envoyer. Si vous souhaitez participer,
vous n’aurez plus qu’à cliquer sur le bouton "*Envoyer*". L’ensemble de la procédure prendra donc **moins d’une minute**.

Si vous avez des questions ou si vous souhaitez nous contacter c’est par [ici](mailto:afgl2@kent.ac.uk).

Merci à tous par avance !`

var englishPresentation = `In the context of our 4th year of study, we must carry out a research project in order to validate our Master's degree.

We are currently working on risk analysis during an online transaction by trying to confirm the identity of the person making the purchase.
At each payment, user’s data qualifying his browser and the transaction itself will be used to create a profile and then analysed by an artificial intelligence that will qualify if there is a correlation between the last reading and the rest of the buyer's profile and thus verify his identity. This project is designed to make online payments more secure.
In order to perform a preliminary training of our artificial intelligence, we need various data and that is why we need you.

By pressing the red button below this text you will allow us to exceptionally access the following data:

* Your operating system and its version
* The brand and model of the hardware you are using and its version.
* The web browser you are using and its version
* The rendering engine software of the browser you are using and its version
* The plug-ins (not browser extensions) currently installed on your browser (if allowed by your browser)
* The state of the "doNotTrack" mode of your browser
* The current size of your browser window
* The list of the different writing fonts installed on your browser
* The list of the different encodings supported by your browser
* The list of the different languages installed on your browser
* The different content types supported by your browser
* The architecture of your processor
* Your current time zone
* Your approximate current position (if authorised by your browser) - *Optional*

Note that all of this data do not in any way allow the identification of a person and that they will be **directly anonymised** and **destroyed at the end of the study** (early September 2019) in order to be **fully compliant with European law** (GDPR).
Once the button is pressed, you will be presented with all the data that will be sent. If you wish to participate, all you have to do is click on the “*Send*” button. Thus the whole process will take **less than a minute**.

If you have any questions or would like to contact us, it is [here](mailto:afgl2@kent.ac.uk).

Thank you !`

class Presentation extends Component {

    constructor(props) {
        super(props)
        this.state = {
            language: "fr",
            languageCallback: props.languageChangedCallback
        }

        this.presentationText = frenchPresentation
    }

    updateLanguage(value) {
        if (value === "0") {
            this.presentationText = frenchPresentation
            this.setState({
                language: "fr"
            })
            this.state.languageCallback("fr")
        } else {
            this.presentationText = englishPresentation
            this.setState({
                language: "en"
            })
            this.state.languageCallback("en")
        }
    }

    render() {
        return (
            <div className="PresentationContainer">
                <div className="TextContainer">
                    <MDReactComponent text={this.presentationText} />
                </div>
                <SegmentedControl
                    name="LanguageSelector"
                    options={[
                        { label: "Français", value: "0", default: true },
                        { label: "English", value: "1" }
                    ]}
                    setValue={newValue => this.updateLanguage(newValue)}
                />
            </div>
        )
    }
}

Presentation.propTypes = {
    languageChangedCallback: PropTypes.func
}
  
Presentation.defaultProps = {
    languageChangedCallback: null
}

export default Presentation