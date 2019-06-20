import React, {Fragment}  from 'react';
import ProductList from './ProductList';
import HeaderBar from './HeaderBar';
import CheckoutForm from './CheckoutForm';
import Footer from './Footer';
import Iframe from 'react-iframe'

function Landing() {
  var [cart, setCartTotal] = React.useState({total: 0})
  var [checkoutStatus, setCheckoutStatus] = React.useState(0)

  function addToCart(prod) {
    setCartTotal({...cart, 
      total: cart.total + prod.price
    })
  }

  function onCheckoutClicked(status) { //0 = list of products, 1 = checkout form, 2 = payment complete
    setCheckoutStatus(status)
  }

  switch(checkoutStatus) {
    case 0:
      return (
        <Fragment>
            <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
            <ProductList addToCart={addToCart}/>
            <Footer/>
        </Fragment>
      );
    case 1:
      return (
        <Fragment>
            <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
            <CheckoutForm cart={cart}/>
        </Fragment>
      );
    case 2: 
      return (
        <Fragment>
            <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
        </Fragment>
      );
    default:
      return("404")
  }
}

export default Landing;