import React from "react";
import axios from "axios";
import "../assets/css/style.css";
class Mehtod extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
  }

  async componentWillMount() {
    let res = await axios.get("http://127.0.0.1:5000/api/methodOpt");
    let data = res.data.data;
    console.log(data);
    this.setState({
      data: data,
    });
  }

  render() {
    return (
      <div>
        <table className="tableMethod">
          <thead>
            <tr>
              <th className="tableMethod th">ID</th>
              <th className="tableMethod th">creator</th>
              <th className="tableMethod th">name</th>
              <th className="tableMethod th">desc</th>
              <th className="tableMethod th">body</th>
            </tr>
          </thead>
          <tbody>
            {this.state.data.map((item, index) => {
              return (
                <tr key={index}>
                  <th className="tableMethod td">{item.id}</th>
                  <th className="tableMethod td">{item.creator}</th>
                  <th className="tableMethod td">{item.name}</th>
                  <th className="tableMethod td">{item.desc}</th>
                  <th className="tableMethod td">
                    <button className="button" onClick={this.detail}>
                      <span>detail</span>
                    </button>
                  </th>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }

  detail = () => {
    console.log("click");
  };
}

export default Mehtod;
