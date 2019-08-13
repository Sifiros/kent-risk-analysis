import React  from 'react';
import startThreeDSProtocol from './ThreeDSProtocolClient.js'
import './res/CheckoutForm.css'
import Footer from './Footer';

class CheckoutForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = { price: props.cart.total }
        this.CcnNumberValid = true //false;
        this.CcDateValid = true //false;
        this.CvvValid = true //false;
        this.paymentResult = 0

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCvvChange = this.handleCvvChange.bind(this);
        this.handleCc_numberChange = this.handleCc_numberChange.bind(this);
        this.handleCc_dateChange = this.handleCc_dateChange.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        console.log(this.state)
        startThreeDSProtocol(this.state)
        .then((response) => response.json())
          .then((response) => {
            if (response.body && response.body.status === "ok")
            setTimeout(() => {
              window.$.featherlight.close()}, 1000)
              window.$('#success_pay').show()
          })
          .catch((error) => {
            window.$('#error_pay').show()
          })
    }

    validCvv(value) {
        if (value.length >= 3 && value.length <= 4)
            return true
        else
            return false
    }

    handleCvvChange(event) {
        this.setState({cvv: event.target.value})
        this.CvvValid = this.validCvv(event.target.value);
    }

    validCreditCard(value) {
        // accept only digits, dashes or spaces
          if (/[^0-9-\s]+/.test(value)) return false;

          // Luhn Algorithm
          var nCheck = 0, nDigit = 0, bEven = false;
          value = value.replace(/\D/g, "");
          for (var n = value.length - 1; n >= 0; n--) {
              var cDigit = value.charAt(n),
                    nDigit = parseInt(cDigit, 10);
              if (bEven) {
                  if ((nDigit *= 2) > 9) nDigit -= 9;
              }
              nCheck += nDigit;
              bEven = !bEven;
          }
          return (nCheck % 10) == 0;
      }

    handleCc_numberChange(event) {
        this.setState({cc_number: event.target.value})
        this.CcnNumberValid = this.validCreditCard(event.target.value);
    }

    validExpirationDate(date) {
        var currentDate = new Date(),
            currentMonth = currentDate.getMonth() + 1,//Zero based index
            currentYear = currentDate.getFullYear(),
            expirationMonth = Number(date.substr(0,2)), //01/
            expirationYear = Number(date.substr(3,date.length)); //starts at 3 after month's slash

        //The expiration date must be atleast one month ahead of current date
        if ((expirationYear < currentYear) || (expirationYear == currentYear && expirationMonth <= currentMonth)) {
            return false;
        } else {
            return true;
        }
    }

    handleCc_dateChange(event) {
        this.setState({cc_date: event.target.value})
        this.CcDateValid = this.validExpirationDate(event.target.value);
    }

    render() {
      const generateLinkList = cart => (
        <div className="form-group col-md-6">
          {cart.list.map((obj, i) =>  <div className="form-row" key={i}>
                                        <div className="form-group col-md-6">
                                          {obj.name}
                                        </div>
                                        <div style={{borderColor:"black"}}></div>
                                        <div className="form-group col-md-6">
                                          {obj.price}€
                                        </div>
                                      </div>)}
          <div className="form-row" style={{marginLeft: "50px", fontSize: "x-large"}}>
            <div className="form-group col-md-6">
              TOTAL
            </div>
            <div className="form-group col-md-6">
              {cart.total}€
            </div>
          </div>
        </div>
      );

        return (
        <div style={{style: "container", marginLeft: "50px", marginRight: "50px"}}>
            <div className="form-row">
              <div className="form-group col-md-6" style={{borderRight:"2px solid black"}}>
              <form onSubmit={this.handleSubmit}>
            <div className="form-row">
              <div className="form-group col-md-4">
                <label htmlFor="inputName">Cardholder name</label>
                <input type="text" required={true} className="form-control" id="inputName" placeholder="John Smith" value={this.state.name} onChange={(event) => this.setState({name: event.target.value})}/>
              </div>
              <div className="form-group col-md-4">
                <label htmlFor="inputEmail4">Email</label>
                <input type="email" required={true} className="form-control" id="inputEmail4" placeholder="Email" value={this.state.email} onChange={(event) => this.setState({email: event.target.value})}/>
              </div>
              <div className="form-group col-md-4">
                <label htmlFor="inputPhone">Phone number</label>
                <input type="tel" required={true} className="form-control" id="inputPhone" placeholder="Phone number" value={this.state.phone_number} onChange={(event) => this.setState({phone_number: event.target.value})}/>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group col-md-5">
                <label htmlFor="inputCardNumber">Credit card number</label>
                <input type="text" className={this.CcnNumberValid ? "form-control" : "form-control invalid"} id="inputCardNumber" placeholder="0000111122223333" maxLength="16" value={this.state.cc_number} onChange={this.handleCc_numberChange}/>
              </div>
              <div className="form-group col-md-5">
                <label htmlFor="inputDate">Expiration date</label>
                <input type="text" placeholder="01/2021" className={this.CcDateValid ? "form-control" : "form-control invalid"}  maxLength="7" id="inputDate" value={this.state.cc_date} onChange={this.handleCc_dateChange}/>
              </div>
              <div className="form-group col-md-2">
                <label htmlFor="inputCCV">CVV</label>
                <input type="number" className={this.CvvValid ? "form-control" : "form-control invalid" } id="inputCCV" maxLength="4" placeholder="666" value={this.state.cvv} onChange={this.handleCvvChange}/>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group col-md-6">
                <label htmlFor="inputAddress">Address</label>
                <input type="text" required={true} className="form-control" id="inputAddress" placeholder="1234 Main St" value={this.state.address} onChange={(event) => this.setState({address: event.target.value})}/>
              </div>
              <div className="form-group col-md-4">
                <label htmlFor="inputCity">City</label>
                <input type="text" required={true} className="form-control" id="inputCity" placeholder="Toulouse" value={this.state.city_name} onChange={(event) => this.setState({city_name: event.target.value})}/>
              </div>
              <div className="form-group col-md-2">
                <label htmlFor="inputZip">Zip</label>
                <input type="text" required={true} className="form-control" id="inputZip" placeholder="31400" value={this.state.postcode} onChange={(event) => this.setState({postcode: event.target.value})}/>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group col-md-12" style={{marginTop: "50px"}}>
                <button type="submit" className="btn btn-primary" disabled={!(this.CvvValid && this.validCreditCard && this.validExpirationDate)}>Proceed to payment</button>
              </div>
            </div>
            </form>
            </div>
                {generateLinkList(this.props.cart)}
                <div id="success_pay" className="form-group col-md-6" style={{display: "none"}}>
                  <p class="success" style={{fontSize: "x-large", textAlign:"center", color:"#73AF55"}}>Payment successful !</p>
                </div>
                <div id="error_pay" className="form-group col-md-6" style={{display: "none"}}>
                  <p class="error" style={{fontSize: "x-large", textAlign:"center", color:"#D06079"}}>Payment failed.</p>
                </div>
            </div>
        </div>)
    }
}

export default CheckoutForm;
