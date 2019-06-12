import React  from 'react';


class CheckoutForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {}
        this.CcnNumberValid = false;
        this.CcDateValid = false;
        this.CvvValid = false;

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCvvChange = this.handleCvvChange.bind(this);
        this.handleCc_numberChange = this.handleCc_numberChange.bind(this);
      }

    handleSubmit(event) {
        event.preventDefault();
        console.log(this.state)
    }

    handleCvvChange(event) {
        this.setState({cvv: event.target.value})
        console.log(event.target)
    }

    handleCc_numberChange(event) {
        this.setState({cc_number: event.target.value})
    }
    
    render() {
        return (
        <div style={{style: "container", marginLeft: "50px", marginRight: "50px"}}>
            <form onSubmit={this.handleSubmit}>
            <div className="form-row">
              <div className="form-group col-md-6">
                <label htmlFor="inputEmail4">Email</label>
                <input type="email" className="form-control" id="inputEmail4" placeholder="Email" value={this.state.email} onChange={(event) => this.setState({email: event.target.value})}/>
              </div>
              <div className="form-group col-md-6">
                <label htmlFor="inputPhone">Phone number</label>
                <input type="tel" className="form-control" id="inputPhone" placeholder="Phone number" value={this.state.phone_number} onChange={(event) => this.setState({phone_number: event.target.value})}/>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group col-md-5">
                <label htmlFor="inputCardNumber">Credit card number</label>
                <input type="text" className={this.CcnNumberValid ? "form-control" : "form-control invalid" } id="inputCardNumber" placeholder="0000111122223333" value={this.state.cc_number} onChange={this.handleCc_numberChange}/>
              </div>
              <div className="form-group col-md-5">
                <label htmlFor="inputDate">Expiration date</label>
                <input type="date" className="form-control" id="inputDate" value={this.state.cc_date} onChange={(event) => this.setState({cc_date: event.target.value})}/>
              </div>
              <div className="form-group col-md-2">
                <label htmlFor="inputCCV">CVV</label>
                <input type="number" className="form-control" id="inputCCV" placeholder="666" value={this.state.cvv} onChange={(event) => this.setState({cvv: event.target.value})}/>
              </div>
            </div>
            <div className="form-group col-md-12">
              <label htmlFor="inputAddress">Address</label>
              <input type="text" className="form-control" id="inputAddress" placeholder="1234 Main St" value={this.state.address} onChange={(event) => this.setState({address: event.target.value})}/>
            </div>
            <div className="form-row">
              <div className="form-group col-md-6">
                <label htmlFor="inputCity">City</label>
                <input type="text" className="form-control" id="inputCity" placeholder="Toulouse" value={this.state.city_name} onChange={(event) => this.setState({city_name: event.target.value})}/>
              </div>
              <div className="form-group col-md-2">
                <label htmlFor="inputZip">Zip</label>
                <input type="text" className="form-control" id="inputZip" placeholder="31400" value={this.state.postcode} onChange={(event) => this.setState({postcode: event.target.value})}/>
              </div>
              <div className="form-group col-md-2">
                <button type="submit" className="btn btn-primary">Proceed to payment</button>
                </div>
            </div>
          </form>
            </div>)
    }
}

export default CheckoutForm;