import React from 'react';
import logo from './logo.svg';
import './static/App.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Home from "./page/home"

function App() {
  return (
    // <div className="App">
    //   <header className="App-header">
    //     <img src={logo} className="App-logo" alt="logo" />

    //     <a
    //       className="App-link"
    //       href="http://www.caoyongqi.top"
    //       target="_blank"
    //       rel="noopener noreferrer"
    //     >
    //       BLOG
    //     </a>
        <Router>
              <div>
                  <Link to="/home">HOME</Link>
              </div>
              <Route exact path="/home" component={Home} />
        </Router>
      // </header>
    // </div>
  );
}

export default App;
