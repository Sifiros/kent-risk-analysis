import React, {Fragment}  from 'react';
import ProductList from './ProductList';
import HeaderBar from './HeaderBar';
import CheckoutForm from './CheckoutForm';
import Footer from './Footer';

function Landing() {
  var [cart, setCartTotal] = React.useState({total: 0})
  var [checkoutStatus, setCheckoutStatus] = React.useState(true)

  function addToCart(prod) {
    cart.total += prod.price
    setCartTotal({...cart, 
      [cart.total]: cart.total + prod.price
    })
  }

  function onCheckoutClicked() {
    setCheckoutStatus(!checkoutStatus)
  }

  if (checkoutStatus) {
    return (
      <Fragment>
          <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
          <CheckoutForm/>
          <Footer/>
      </Fragment>
    );
  } else {
    return (
      <Fragment>
          <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
          <ProductList addToCart={addToCart}/>
          <Footer/>
      </Fragment>
    );
  }
}

export default Landing;