import React from 'react';
import { RaisedButton } from 'material-ui';
import IconShoppingCart from 'material-ui/svg-icons/action/shopping-cart';
import './res/HeaderBar.css'

function HeaderBar(props) {
  if (props.status) {
    return (<header>
      <div className="Bar"/>
      <div className="Title">
        <div className="Logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="60" viewBox="0 0 20 20"><path d="M20 4H4v2h16V4zm1 10v-2l-1-5H4l-1 5v2h1v6h10v-6h4v6h2v-6h1zm-9 4H6v-4h6v4z"/></svg>								
          Awesome Retailer Demo
        </div>
        <RaisedButton
            label="Return"
            onClick={props.onCheckoutClicked}
            backgroundColor={"#10101010"}
            labelColor={"#212121"}  />
      </div>
      <h2 className="row divided">
        <span>Buying Products</span>
      </h2>
  </header>)
  } else {
    return (<header>
      <div className="Bar"/>
      <div className="Title">
        <div className="Logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="60" viewBox="0 0 20 20"><path d="M20 4H4v2h16V4zm1 10v-2l-1-5H4l-1 5v2h1v6h10v-6h4v6h2v-6h1zm-9 4H6v-4h6v4z"/></svg>								
          Awesome Retailer Demo
        </div>
        <RaisedButton
            label={"Checkout (" + props.cart.total + "€)"}
            onClick={props.onCheckoutClicked}
            icon={<IconShoppingCart />}
            backgroundColor={"#10101010"}
            labelColor={"#212121"}/>
      </div>
      <h2 className="row divided">
        <span>Available Products</span>
      </h2>
  </header>)
  }
}

export default HeaderBar;