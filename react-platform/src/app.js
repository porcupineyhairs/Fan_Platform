import React from "react";
import { createStore } from "redux";
import { Povider, connect } from "react-redux";

class Counter extends React.Component {
  render() {
    // 计数 通过stroe的state黄给porps
    const value = this.props.value;
    //将修改数据的事件或方法传入props
    const onAddClick = this.props.onAddClick;

    return (
      <div>
        <h1>计数{value}</h1>
        <button onClick={onAddClick}>+1</button>
        <button>-1</button>
      </div>
    );
  }
}

const addAction = {
  type: "add",
};

ActionObj = {
  add: function (state, action) {
    state.num++;
    return state;
  },
};

function reducer(state = { num: 0 }, action) {
  state = ActionObj[action.type](action);
  return state;
}
//数据仓库
const store = createStore(reducer);

// 将state 映射到props函数
function mapStateToProps(state) {
  return { value: state.num };
}
function mapDispatchToProps(dispatch) {
  return {
    onAddClick: () => {
      dispatch(addAction);
    },
  };
}
//关联映射到组件
App = connect(mapStateToProps, mapDispatchToProps)(Counter);

export default APP;
