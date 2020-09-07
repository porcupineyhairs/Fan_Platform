import React from "react";
import Mehtod from "./component/method.js";
import "./assets/css/style.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      newData: null,
      nevList: ["F1", "F2", "F3", "F4"],
      tabeIndex: 0,
    };
  }

  render() {
    return (
      // <div className="nav">
      //   <div>
      //     {this.state.nevList.map((item, index) => {
      //       if (index === this.state.tabeIndex) {
      //         return (
      //           <div className="navItem active" key={index}>
      //             {item}
      //           </div>
      //         );
      //       } else {
      //         return (
      //           <div className="navItem" key={index}>
      //             {item}
      //           </div>
      //         );
      //       }
      //     })}
      //   </div>
      //   <div className="nav">
          <Mehtod />
    );
  }
}

export default App;
