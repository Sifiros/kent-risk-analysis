import React  from 'react';

function Validation(props) {
    console.log(props)
    if (props.success === 1)
        return (<div>
        <div id="success_pay" style={{marginLeft: "50vh", marginRight:"50vh"}}>
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130.2 130.2">
                <circle class="path circle" fill="none" stroke="#73AF55" stroke-width="6" stroke-miterlimit="10" cx="65.1" cy="65.1" r="62.1"/>
                <polyline class="path check" fill="none" stroke="#73AF55" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10"
                    points="100.2,40.2 51.5,88.8 29.8,67.5 " />
            </svg>
            <p class="success" style={{fontSize: "xx-large", textAlign:"center"}}>Payment Successful !</p>
        </div><script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha256-3edrmyuQ0w65f8gfBsqowzjJe2iM6n0nKciPUp8y+7E="
            crossorigin="anonymous"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/less.js/3.0.2/less.min.js"></script></div>)
    else if (props.success === 2)
        return(<div>
            <div id="error_pay" style={{marginLeft: "50vh", marginRight:"50vh"}}>
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130.2 130.2">
                    <circle class="path circle" fill="none" stroke="#D06079" stroke-width="6" stroke-miterlimit="10" cx="65.1" cy="65.1" r="62.1"/>
                    <line class="path line" fill="none" stroke="#D06079" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" x1="34.4"
                        y1="37.9" x2="95.8" y2="92.3" />
                    <line class="path line" fill="none" stroke="#D06079" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" x1="95.8"
                        y1="38" x2="34.4" y2="92.2" />
                </svg>
                <p class="error" style={{fontSize: "xx-large", textAlign:"center"}}>Payment failed.</p>
            </div><script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha256-3edrmyuQ0w65f8gfBsqowzjJe2iM6n0nKciPUp8y+7E="
                crossorigin="anonymous"></script>
            <script src="//cdnjs.cloudflare.com/ajax/libs/less.js/3.0.2/less.min.js"></script></div>)
    else
        return(<div style={{marginLeft: "50vh", marginRight:"50vh", fontSize:"50px"}}>Processing payment</div>)
}

export default Validation;