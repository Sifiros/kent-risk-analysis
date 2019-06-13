import React from 'react';
import list from './res/products.js'

import './res/ProductList.css'

import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';
import { RaisedButton } from 'material-ui';

const imgStyle = {
  maxHeight: '100%',
  verticalAlign: 'middle',
  padding: '4px 0',
  border: '1px',
};

const iconStyle = {
  paddingLeft: '30px',
};

const ProductList = ({ addToCart }) => (
    <div id="products" className="row" style={{style: "container", marginLeft: "50px", marginRight: "50px"}}>
    <Table selectable={false}>
      <TableHeader adjustForCheckbox={true} displaySelectAll={false}>
        <TableRow>
          <TableHeaderColumn>Image</TableHeaderColumn>
          <TableHeaderColumn>Name</TableHeaderColumn>
          <TableHeaderColumn>Price</TableHeaderColumn>
          <TableHeaderColumn />
        </TableRow>
      </TableHeader>
      <TableBody>
        {list.map(prod => (
          <TableRow key={prod.name}>
            <TableRowColumn>
              <img src={prod.image} alt="picture" style={imgStyle} />
            </TableRowColumn>
            <TableRowColumn>{prod.name}</TableRowColumn>
            <TableRowColumn><b>{prod.price}€</b></TableRowColumn>
            <TableRowColumn>
                <RaisedButton
                  label="Add to cart"
                  onClick={() => addToCart(prod)}
                />
            </TableRowColumn>
          </TableRow>
        ))}
      </TableBody>
    </Table>
</div>)


export default ProductList;