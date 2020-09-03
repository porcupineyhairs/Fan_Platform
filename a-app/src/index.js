import React from "react";
import ReactDOM from "react-dom";
import "./static/index.css";

// let  elementStyle = {
//   background:"skyblue"
// }

// let element =(
//   <div>
//       <h1 style={elementStyle}>hellowoeld</h1>
//   </div>
// )

// let classStr = ["aaa","bbb"].join(" ")
// let element2 = (
//   <div className="abc">
//     {/*  這是註釋  */}
//     <h1 className="redBg" >helloworld</h1>
//   </div>
// )

function Childcom(props) {
  let title = <h2>我是标题</h2>;
  let weather = props.weather;
  let isOk = weather === "下雨" ? "不出门" : "出门";

  return (
    <div>
      <h1>helloworld</h1>
      {title}
      <div>
        是否出门?
        <span>{isOk}</span>
      </div>
    </div>
  );
}

class HelloWorld extends React.Component {
  render() {
    console.log(this.props.weather);
    return (
      <div>
        <Childcom weather={this.props.weather} />
      </div>
    );
  }
}
//=========================================================

class Clock extends React.Component {
  constructor(props) {
    super(props);
    // 初始化数据,
    //state
    this.state = {
      time: new Date().toLocaleTimeString(),
    };
  }
  render() {
    return (
      <div>
        <h1>当前时间{this.state.time}</h1>
      </div>
    );
  }

  //生命周期函数 组件渲染完成时调用, setState 修改state数据, 直接修改不会渲染
  componentDidMount() {
    setInterval(() => {
      this.setState({
        time: new Date().toLocaleTimeString(),
      });
    }, 1000);
  }
}

class Tab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      c1: "content",
      c2: "content",
    };
    this.clickEvent = this.clickEvent.bind(this);
  }

  clickEvent(e) {
    console.log(e.target);
    console.log(e.target.dataset.index);
    let index = e.target.dataset.index;
    if (index === "1") {
      this.setState({
        c1: "content active",
        c2: "content",
      });
    } else {
      this.setState({
        c1: "content",
        c2: "content active",
      });
    }
  }

  render() {
    return (
      <div>
        <button data-index="1" onClick={this.clickEvent}>
          content1
        </button>
        <button data-index="2" onClick={this.clickEvent}>
          content2
        </button>
        <div className={this.state.c1}>内容1</div>
        <div className={this.state.c2}>内容2 </div>
      </div>
    );
  }
}

//=======================props===========================

//  父传递给子组件数据, 单向流动, 不能子传父
// 可以是任意的类型
// 可设置默认值
// Hello.defaultPorps = {name:"cyq"}

// 可传递函数

//在父元素中使用state 去控制子元素props 从而达到父元素数据传递给子元素

class ParentCom extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isActive: true,
    };
    this.change = this.change.bind(this);
  }
  change() {
    this.setState({
      isActive: !this.state.isActive,
    });
  }

  render() {
    return (
      <div>
        <button onClick={this.change}>控制子元素显示</button>
        <ChildCom isActive={this.state.isActive} />
      </div>
    );
  }
}

class ChildCom extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let ele = null;
    console.log(this.props);
    if (this.props.isActive) {
      ele = "active";
    } else {
      ele = "";
    }

    return (
      <div className={"content " + ele}>
        <h1>HelloWorld</h1>
      </div>
    );
  }
}

//=============================子传父==========================

class Master extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      salve: null,
    };
  }
  setSalveData = (data) => {
    this.setState({
      salve: data,
    });
  };

  render() {
    return (
      <div>
        <h1>子元素传递给父元素数据: {this.state.salve}</h1>
        <Salve setSalveData={this.setSalveData} />
      </div>
    );
  }
}

class Salve extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      msg: "hello",
    };
    this.sendData = this.sendData.bind(this);
  }

  sendData() {
    console.log(this.state.msg);
    this.props.setSalveData(this.state.msg);
  }

  render() {
    return (
      <div>
        <button onClick={this.sendData}>传递 hello 给父元素</button>
        <button
          onClick={() => {
            this.props.setSalveData(this.state.msg);
          }}
        >
          传递 hello 给父元素
        </button>
      </div>
    );
  }
}

// =====================事件=========================

//react 返回事件是代理的原生对象, 想看具体值,必须之间输出时间对象的属性

class P extends React.Component {
  constructor(props) {
    super(props);
  }
  clickEvent = (e) => {
    console.log(e);
    // e.preventDefault(); //组织默认
  };

  render() {
    return (
      <div>
        <form action="http://www.caoyongqi.top">
          <div onClick={this.clickEvent}>
            <div>
              <h1>HelloWorld</h1>
              <div>
                <button onClick={this.clickEvent}></button>
              </div>
            </div>
          </div>
        </form>

        <button
          onClick={(e) => {
            this.clickEvent("hello", e);
          }}
        >
          click
        </button>
      </div>
    );
  }
}

//===================条件渲染 列表渲染=========================

function UserGreat(props) {
  return <h1>欢迎登录</h1>;
}
function UserLogin(props) {
  return <h1>请登录</h1>;
}

class A extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogin: true,
    };
  }
  //   条件运算
  render() {
    let ele = null;

    if (this.state.isLogin) {
      ele = <UserGreat />;
    } else {
      ele = <UserLogin />;
    }

    return (
      <div>
        {ele}
        <hr />
        <hr />
        {this.state.isLogin ? <UserGreat /> : <UserLogin />}
      </div>
    );
  }
}

//列表渲染
let arr = ["A", "B", "C"];

class Arr extends React.Component {
  constructor(props) {
    super(props);
  }

  event = (num) => {
    alert(num);
  };

  render() {
    return (
      <div>
        <ul>
          {arr.map((iterm, index) => {
            return (
              <li
                key={index}
                onClick={(e) => {
                  this.event({ iterm });
                }}
              >
                <p>{iterm}</p>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
}

ReactDOM.render(<Arr />, document.getElementById("root"));
