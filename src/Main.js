import React from "react";
import "./css/table.scss"
import Navbar from "./components/Navbar";
import IfaceRow from "./components/IfaceRow";



export default class Main extends React.Component {
    render() {
        return (
        <div>
        <Navbar></Navbar>
        <div className="content-wrapper">
          <section className="content">
            <div className="container-fluid">
              <IfaceRow></IfaceRow>
            </div>
          </section>
        </div>
        </div>)
    }
}