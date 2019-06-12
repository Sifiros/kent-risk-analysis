import React, {Fragment}  from 'react';
import ProductList from './ProductList';
import HeaderBar from './HeaderBar';
import CheckoutForm from './CheckoutForm';

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
      </Fragment>
    );
  } else {
    return (
      <Fragment>
          <HeaderBar cart={cart} status={checkoutStatus} onCheckoutClicked={onCheckoutClicked}/>
          <ProductList addToCart={addToCart}/>
      </Fragment>
    );
  }
}

export default Landing;