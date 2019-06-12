import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Landing from './Landing';
import * as serviceWorker from './serviceWorker';
import { getMuiTheme, MuiThemeProvider } from 'material-ui/styles';
import * as colors from 'material-ui/styles/colors';

const muiTheme = getMuiTheme({
    palette: {
      primary1Color: colors.redA200,
    },
  });

ReactDOM.render(
    <MuiThemeProvider muiTheme={muiTheme}>
        <Landing />
    </MuiThemeProvider>,
    document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
