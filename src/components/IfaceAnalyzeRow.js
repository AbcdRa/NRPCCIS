import React from 'react';
import axios from 'axios';

export default class IfaceAnalyzeRow extends React.Component {
  
  flows_count = 0
  flows_analyzed = 0
  state = {flows: [], current_model_name:''}


  updateState() {
    const ajax_url = `http://127.0.0.1:7778/get_flows?dev_id=${this.props.iface_id}`
    axios.get(ajax_url)
        .then(res => {
          console.log("AJAX HUI")
          console.log(this.state)
          this.setState((state)=>{return {flows:res.data.data}});
          console.log(this.state)
    })
    axios.get(`http://127.0.0.1:7778/get_current_model`)
    .then(res => {
        const current_model_name_new = res.data;
        this.setState((state)=>{return {current_model_name:current_model_name_new}});
    })
  }

  componentDidMount() {
    this.updateState()
    setInterval(()=>{this.updateState()}, 10000);
  }
  
  render() {
    this.flows_count = this.state.flows.length
    console.log("AJAX_DEBUG flows update")
    console.log(this.flows)
    this.flows_analyzed = this.state.flows.filter( flow => this.state.current_model_name in flow)
    this.flows_danger = this.flows_analyzed.filter(flow => flow[this.state.current_model_name] !== 'BENIGN')
      return (
          <div className="card">
            <div className="card-header">
              <h5 className="card-title">Анализ потоков</h5>

              <div className="card-tools">
                <button type="button" className="btn btn-tool" data-card-widget="collapse">
                  <i className="fas fa-minus"></i>
                </button>
                <div className="btn-group">
                  <button type="button" className="btn btn-tool dropdown-toggle" data-toggle="dropdown">
                    <i className="fas fa-wrench"></i>
                  </button>
                  <div className="dropdown-menu dropdown-menu-right" role="menu">
                    <a href="/#" className="dropdown-item">Action</a>
                    <a href="/#" className="dropdown-item">Another action</a>
                    <a href="/#" className="dropdown-item">Something else here</a>
                    <a href="/#" className="dropdown-divider">WTF</a>
                    <a href="/#" className="dropdown-item">Separated link</a>
                  </div>
                </div>
                <button type="button" className="btn btn-tool" data-card-widget="remove">
                  <i className="fas fa-times"></i>
                </button>
              </div>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col">
                  <p className="text-center">
                    <strong>Проаниализировано потоков</strong>
                  </p>

                  <div className="progress-group">
                    Количество сохраненных потоков
                    <span className="float-right"><b>{this.flows_count}</b></span>
                    <div className="progress progress-sm">
                      <div className="progress-bar bg-primary" style={{"width": "100%"}}></div>
                    </div>
                  </div>
                  <div className="progress-group">
                    Обработано потоков
                    <span className="float-right"><b>{this.flows_analyzed.length}</b>/{this.flows_count}</span>
                    <div className="progress progress-sm">
                      <div className="progress-bar bg-success" 
                        style={{"width": 100-100*((this.flows_count-this.flows_analyzed.length)/this.flows_count) + "%"}}></div>
                    </div>
                  </div>
                  <div className="progress-group">
                    <span className="progress-text">Обнаружено угроз</span>
                    <span className="float-right"><b>{this.flows_danger.length}</b>/{this.flows_analyzed.length}</span>
                    <div className="progress progress-sm">
                      <div className="progress-bar bg-danger" 
                      style={{"width": 100-100*((this.flows_analyzed.length-this.flows_danger.length)/this.flows_analyzed.length) + "%"}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="card-footer">

              <div class="card-header border-transparent">
                <h3 class="card-title">Обнаруженные угрозы</h3>
              </div>
              <div className='card'>
              <div class="card-body p-0">
                <div class="table-responsive">
                  <table class="table m-0">
                    <thead>
                    <tr>
                      <th>Тип угрозы</th>
                      <th>Id потока</th>
                      <th>Выбранная модель</th>
                      <th>Время</th>
                    </tr>
                    </thead>
                    <tbody>
                    {this.flows_danger.map(flow => <tr>
                      <td><span class="badge badge-danger">{flow[this.state.current_model_name]}</span></td>
                      <td>{flow['id']}</td>
                      <td>{this.state.current_model_name}</td>
                      <td>
                        <div class="sparkbar" data-color="#00a65a" data-height="20">{flow['timestamp']}</div>
                      </td>
                    </tr>
                    )}
                    
                    </tbody>
                  </table>
                </div>
              </div>
              </div>
            </div>
          </div>
      )
  }
  }