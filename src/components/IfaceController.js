import React from "react";
import axios from "axios";

export default class IfaceController extends React.Component {
    state = {isMonitoring:false, analyzeStopFlag:true}

    constructor(props) {
        super(props)
        this.URLRequestPackets = 'http://127.0.0.1:7778/get_flows?dev_id=' + this.props.iface_id
        this.URLRequestMonitoring = 'http://127.0.0.1:7778/start_monitoring?dev_id=' + this.props.iface_id 
        this.URLRequestIsMonitoring = 'http://127.0.0.1:7778/is_monitoring?dev_id=' + this.props.iface_id
        this.URLRequestStopMonitoring = 'http://127.0.0.1:7778/stop_monitoring?dev_id=' + this.props.iface_id 
        this.URLRequestStartAnalyze = 'http://127.0.0.1:7778/start_analyze?dev_id=' + this.props.iface_id 
    }

    startMonitoring() {
        axios.get(this.URLRequestMonitoring)
        .then(res => {
          console.log(res);
        })
      }
    
    startAnalyze() {
    this.setState({analyzeStopFlag:false})
    axios.get(this.URLRequestStartAnalyze)
    .then(res => {
        this.setState({analyzeStopFlag:true})
    })
    }

    stopMonitoring() {
    console.log(this.URLRequestStopMonitoring)
    axios.get(this.URLRequestStopMonitoring)
    .then(res => {
        console.log(res);
    })
    }

    isMonitoring() {
    axios.get(this.URLRequestIsMonitoring)
    .then(res => {
        this.setState({isMonitoring:res.data.is_monitoring})
    })
    return this.isMonitoring
    }
    
    componentDidMount() {
        this.isMonitoring();
        setInterval(()=>{this.isMonitoring()}, 10000);
    }

    render() {
        return (<div className="d-flex justify-content-between">
        <span>
        <button 
          className={this.state.isMonitoring? 'btn btn-dark':'btn btn-light text-success'} 
          disabled={this.state.isMonitoring} onClick={()=>{this.startMonitoring()}}>Начать мониторинг</button>
        <button 
          className={!this.state.isMonitoring? 'btn btn-dark':'btn btn-light text-danger'} 
          disabled={!this.state.isMonitoring} onClick={()=>{this.stopMonitoring()}}>Закончить мониторинг</button>
        </span>


        <span>
          <div className="btn-group" role="group" aria-label="Basic example">
          <button 
            className={!this.state.analyzeStopFlag? 'btn btn-dark':'btn btn-light text-success'} 
            disabled={!this.state.analyzeStopFlag} onClick={()=>{this.startAnalyze()}}>Начать анализ</button>
          </div>
        </span>
        
      </div>)
    }
}