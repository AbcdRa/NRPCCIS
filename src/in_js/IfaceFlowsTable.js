

export default function getInjectedScriptText(ajax_url) {
    
    const InjectedScriptText = `if (typeof INITONCE === 'undefined') { 
        new DataTable("#example2", {
          "paging": true,
          "lengthChange": true,
          'scrollX': true,
          "searching": false,
          "ordering": true,
          "info": true,
          "ajax": '${ajax_url}',
          columns: [{"data":"id"},{"data":"created_time"},{"data":"src_ip"},{"data":"dst_ip"},{"data":"src_port"},{"data":"dst_port"},{"data":"src_mac"},{"data":"dst_mac"},{"data":"protocol"},{"data":"timestamp"},{"data":"flow_duration"},{"data":"flow_byts_s"},{"data":"flow_pkts_s"},{"data":"fwd_pkts_s"},{"data":"bwd_pkts_s"},{"data":"tot_fwd_pkts"},{"data":"tot_bwd_pkts"},{"data":"totlen_fwd_pkts"},{"data":"totlen_bwd_pkts"},{"data":"fwd_pkt_len_max"},{"data":"fwd_pkt_len_min"},{"data":"fwd_pkt_len_mean"},{"data":"fwd_pkt_len_std"},{"data":"bwd_pkt_len_max"},{"data":"bwd_pkt_len_min"},{"data":"bwd_pkt_len_mean"},{"data":"bwd_pkt_len_std"},{"data":"pkt_len_max"},{"data":"pkt_len_min"},{"data":"pkt_len_mean"},{"data":"pkt_len_std"},{"data":"pkt_len_var"},{"data":"fwd_header_len"},{"data":"bwd_header_len"},{"data":"fwd_seg_size_min"},{"data":"fwd_act_data_pkts"},{"data":"flow_iat_mean"},{"data":"flow_iat_max"},{"data":"flow_iat_min"},{"data":"flow_iat_std"},{"data":"fwd_iat_tot"},{"data":"fwd_iat_max"},{"data":"fwd_iat_min"},{"data":"fwd_iat_mean"},{"data":"fwd_iat_std"},{"data":"bwd_iat_tot"},{"data":"bwd_iat_max"},{"data":"bwd_iat_min"},{"data":"bwd_iat_mean"},{"data":"bwd_iat_std"},{"data":"fwd_psh_flags"},{"data":"bwd_psh_flags"},{"data":"fwd_urg_flags"},{"data":"bwd_urg_flags"},{"data":"fin_flag_cnt"},{"data":"syn_flag_cnt"},{"data":"rst_flag_cnt"},{"data":"psh_flag_cnt"},{"data":"ack_flag_cnt"},{"data":"urg_flag_cnt"},{"data":"ece_flag_cnt"},{"data":"down_up_ratio"},{"data":"pkt_size_avg"},{"data":"init_fwd_win_byts"},{"data":"init_bwd_win_byts"},{"data":"active_max"},{"data":"active_min"},{"data":"active_mean"},{"data":"active_std"},{"data":"idle_max"},{"data":"idle_min"},{"data":"idle_mean"},{"data":"idle_std"},{"data":"fwd_byts_b_avg"},{"data":"fwd_pkts_b_avg"},{"data":"bwd_byts_b_avg"},{"data":"bwd_pkts_b_avg"},{"data":"fwd_blk_rate_avg"},{"data":"bwd_blk_rate_avg"},{"data":"fwd_seg_size_avg"},{"data":"bwd_seg_size_avg"},{"data":"cwe_flag_count"},{"data":"subflow_fwd_pkts"},{"data":"subflow_bwd_pkts"},{"data":"subflow_fwd_byts"},{"data":"subflow_bwd_byts"}]
        });
     }
    var INITONCE = true;
    `
    return InjectedScriptText
}


