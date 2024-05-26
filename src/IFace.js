import React from 'react';
import withRouter from './withRouters';
import DataTable from 'react-data-table-component';
import './css/iface.scss'
import axios from 'axios';
import IfaceFlow from './components/IfaceFlow';
import Navbar from './components/Navbar';
import useScript from './hooks/useScript';





class IFacePacketTable extends React.Component {

  state = {packets:[]}

  constructor(props) {
      super(props)
      this.URLRequestPackets = 'http://127.0.0.1:7778/get_flows?dev_id=' + this.props.params.iface_id + '&page='
      this.URLRequestMonitoring = 'http://127.0.0.1:7778/start_monitoring?dev_id=' + this.props.params.iface_id 
      this.URLRequestIsMonitoring = 'http://127.0.0.1:7778/is_monitoring?dev_id=' + this.props.params.iface_id
      this.URLRequestStopMonitoring = 'http://127.0.0.1:7778/stop_monitoring?dev_id=' + this.props.params.iface_id 
  }


  startMonitoring() {
    console.log(this.URLRequestMonitoring)
    axios.get(this.URLRequestMonitoring)
    .then(res => {
      console.log(res);
    })
  }

  stopMonitoring() {
    console.log(this.URLRequestStopMonitoring)
    axios.get(this.URLRequestStopMonitoring)
    .then(res => {
      console.log(res);
    })
  }

  componentDidMount() {
    const COLUMNS = ["id", "created_time","src_ip","dst_ip","src_port","dst_port","src_mac","dst_mac","protocol","timestamp","flow_duration",
    "flow_byts_s","flow_pkts_s","fwd_pkts_s","bwd_pkts_s","tot_fwd_pkts","tot_bwd_pkts","totlen_fwd_pkts","totlen_bwd_pkts",
    "fwd_pkt_len_max","fwd_pkt_len_min","fwd_pkt_len_mean","fwd_pkt_len_std","bwd_pkt_len_max","bwd_pkt_len_min","bwd_pkt_len_mean",
    "bwd_pkt_len_std","pkt_len_max","pkt_len_min","pkt_len_mean","pkt_len_std","pkt_len_var","fwd_header_len","bwd_header_len",
    "fwd_seg_size_min","fwd_act_data_pkts","flow_iat_mean","flow_iat_max","flow_iat_min","flow_iat_std","fwd_iat_tot","fwd_iat_max",
    "fwd_iat_min","fwd_iat_mean","fwd_iat_std","bwd_iat_tot","bwd_iat_max","bwd_iat_min","bwd_iat_mean","bwd_iat_std","fwd_psh_flags",
    "bwd_psh_flags","fwd_urg_flags","bwd_urg_flags","fin_flag_cnt","syn_flag_cnt","rst_flag_cnt","psh_flag_cnt","ack_flag_cnt",
    "urg_flag_cnt","ece_flag_cnt","down_up_ratio","pkt_size_avg","init_fwd_win_byts","init_bwd_win_byts","active_max",
    "active_min","active_mean","active_std","idle_max","idle_min","idle_mean","idle_std","fwd_byts_b_avg","fwd_pkts_b_avg",
    "bwd_byts_b_avg","bwd_pkts_b_avg","fwd_blk_rate_avg","bwd_blk_rate_avg","fwd_seg_size_avg","bwd_seg_size_avg","cwe_flag_count",
    "subflow_fwd_pkts","subflow_bwd_pkts","subflow_fwd_byts","subflow_bwd_byts"]
    const TCOLUMNS = COLUMNS.map(el => {return {data:el}})

    let script = document.createElement("script");
    
    script.text = `
    if (typeof INITONCE !== 'undefined') { 
    new DataTable("#example2", {
      "paging": true,
      "lengthChange": true,
      'scrollX': true,
      "searching": false,
      "ordering": true,
      "info": true,
      "ajax": 'http://127.0.0.1:7778/get_flows?dev_id=10',
      columns: ` + JSON.stringify(TCOLUMNS) + 
      `
    });
    }
    var INITONCE = true;
    `;
    document.body.appendChild(script);
}



  render() {
    return (<div>
      <Navbar></Navbar>
      <div className="content-wrapper">
        <section className="content">
          <div className="container-fluid">
            <IfaceFlow></IfaceFlow>
          </div>
        </section>
      </div>
      </div>
      )
    
  }
}

export default withRouter(IFacePacketTable)