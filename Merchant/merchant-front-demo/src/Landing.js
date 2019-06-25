import React, {Fragment}  from 'react';
import ProductList from './ProductList';
import HeaderBar from './HeaderBar';
import CheckoutForm from './CheckoutForm';
import Footer from './Footer';
import Validation from './Validation';

function Landing() {
  var [cart, setCartTotal] = React.useState({total: 0, list: []})
  var [checkoutStatus, setCheckoutStatus] = React.useState(0)
  var [paymentStatus, setPaymentStatus] = React.useState(false)

  function addToCart(prod) {
    cart.list.push(prod)
    setCartTotal({...cart, 
      total: cart.total + prod.price,
      list: cart.list
    })
  }

  function onCheckoutClicked(status) { //0 = list of products, 1 = checkout form, 2 = payment complete
    setCheckoutStatus(status)
  }

  function onPaymentDone(status) {
    setPaymentStatus(status)
    onCheckoutClicked(2)
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
            <CheckoutForm cart={cart} onPaymentDone={onPaymentDone}/>
        </Fragment>
      );
    case 2: 
      return (
        <Fragment>
            <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
            <Validation success={paymentStatus}/>
        </Fragment>
      );
    default:
      return("404")
  }
}

export default Landing;