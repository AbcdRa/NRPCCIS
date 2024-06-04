import React from 'react';
import withRouter from './withRouters';
import './css/iface.scss'
import IfaceFlow from './components/IfaceFlow';
import Navbar from './components/Navbar';
import IfaceController from './components/IfaceController';
import getInjectedScriptText from './in_js/IfaceFlowsTable';
import IfaceAnalyzeRow from './components/IfaceAnalyzeRow'
import axios from 'axios';

class IFace extends React.Component {

  iface_id = 1

  constructor(props) {
      super(props)
      this.iface_id = this.props.params.iface_id;
  }


  componentDidMount() {
    const ajax_url = `http://127.0.0.1:7778/get_flows?dev_id=${this.iface_id}`
    try {
      let script = document.createElement("script");
      script.text = getInjectedScriptText(ajax_url);
      document.body.appendChild(script);
    } catch (err) {
      console.error(err);
    }
}

  render() {
    return (
    <div>
      <Navbar></Navbar>
      <div className="content-wrapper">
        <section className="content">
          <div className="container-fluid">
            <IfaceController iface_id={this.iface_id}></IfaceController>
            <IfaceFlow ></IfaceFlow>
            <IfaceAnalyzeRow iface_id={this.iface_id}></IfaceAnalyzeRow>
          </div>
        </section>
      </div>
    </div>
      )
    
  }
}

export default withRouter(IFace)