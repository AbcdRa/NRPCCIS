import React from "react";
import "./css/table.scss"
import Navbar from "./components/Navbar";
import MainIfaceRow from "./components/MainIfaceRow";
import ModelList from "./components/MainModelList";



export default class Main extends React.Component {
    render() {
        return (
        <div>
        <Navbar></Navbar>
        <div className="content-wrapper">
          <section className="content">
            <div className="container-fluid">
              <MainIfaceRow></MainIfaceRow>
              <ModelList></ModelList>
            </div>
          </section>
        </div>
        </div>)
    }
}