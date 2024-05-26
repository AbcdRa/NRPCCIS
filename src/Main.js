import React from "react";
import "./css/table.scss"
import Navbar from "./components/Navbar";
import IfaceRow from "./components/IfaceRow";
import ModelList from "./components/ModelList";



export default class Main extends React.Component {
    render() {
        return (
        <div>
        <Navbar></Navbar>
        <div className="content-wrapper">
          <section className="content">
            <div className="container-fluid">
              <IfaceRow></IfaceRow>
              <ModelList></ModelList>
            </div>
          </section>
        </div>
        </div>)
    }
}