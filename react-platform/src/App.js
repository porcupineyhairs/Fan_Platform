import React from "react";
import Mehtod from "./component/method.js";
import {
  BrowserRouter as Router,
  Link,
  Route,
  Redirect,
  Switch,
} from "react-router-dom";

import "./assets/css/style.css";

class Home extends React.Component {
  render() {
    console.log(this.props)
    return <div>首页</div>;
  }
}
class Me extends React.Component {
  render() {
    console.log(this.props);
    return <div>个人</div>;
  }
}
class Product extends React.Component {
  render() {
    return <div>产品</div>;
  }
}
class News extends React.Component {
  render() {
    return <div>新闻 ID:{this.props.match.params.id}</div>;
  }
}

class Form extends React.Component {
  render() {
    let pathObj = {
      pathname: "/logininfo",
      state: {
        loginState: "success",
      },
    };
    return (
      <div>
        <h1>表单</h1>
        <Link to={pathObj}>跳转</Link>

        <button onClick={this.clickEvent}>按钮跳转</button>
      </div>
    );
  }
  clickEvent = ()=>{
      console.log(this.props)
      this.props.history.push('/',{msg:'hello'})
  }
}

class LoginInfo extends React.Component {
  render() {
    console.log(this.props);
    if (this.props.location.state.loginState === "success") {
      return <Redirect to="/admin" />;
    } else {
      return <Redirect to="/login" />;
    }
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let meObj = {
      pathname: "/me",
      search: "?username=admin",
      hash: "#abc",
      state: { msg: "helloworld" },
    };
    return (
      <div id="app">
        <Router>
          <div className="nav">
            <Link to="/">Home</Link>
            <Link to="/product">Product</Link>
            <Link to={meObj} replace>
              Me
            </Link>
            <Link to="/method">mthod</Link>
            <Link to="/news/123">news</Link>
            <Link to="/form">form</Link>
          </div>
          <Route path="/" exact component={Home} />
          <Route path="/product" component={Product} />
          <Route path="/me" component={Me} />
          <Route path="/method" component={Mehtod} />
          <Route path="/news/:id" component={News} />
          <Route path="/form" component={Form} />
          <Route path="/logininfo" component={LoginInfo} />
          <Route path="/admin " exact component={() => <div>admin</div>} />
          <Route path="/login " exact component={() => <div>login</div>} />

          <Switch> //匹配第一个 下面的而不会被匹配到
            <Route path="/abc " exact component={() => <div>admin</div>} />
            <Route path="/abc " exact component={() => <div>login</div>} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
