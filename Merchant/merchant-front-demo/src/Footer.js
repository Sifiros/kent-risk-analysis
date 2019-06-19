import React from 'react';
import './res/Footer.css'

const generateLinkList = config => (
  <div className="linkList">
    <h4>{config.title}</h4>
    {config.links && config.links.map((link, i) => <span className="footerspan" key={i}>{link}</span>)}
  </div>
);

export default () => (
  <footer>
    <div className="row footerrow">
      {generateLinkList({
        title: 'Merchant Front',
        links: ['About', 'Terms and Conditions', 'Privacy Policy', 'Contact us'],
      })}
      {generateLinkList({
        title: 'Customer Care',
        links: ['Contact Us', 'FAQs', 'Delivery & Shipping', 'Returns Policy'],
      })}
    </div>
  </footer>
);
