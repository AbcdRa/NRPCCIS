import React from "react";
import "./css/table.scss"
import axios from "axios"
import Navbar from "./components/Navbar";
import Contents from "./components/Contents";



export default class Main extends React.Component {
    state = {ifaces:[]}

    componentDidMount() {
      axios.get(`http://127.0.0.1:7778/get_ifaces`)
        .then(res => {
          const ifaces = res.data;
          this.setState({ ifaces });
        })
    }
  

    render() {
      
        return (
        <div>
        <Navbar></Navbar>
        <Contents></Contents>
        </div>)
    }
}