import React from 'react';



class Contents extends React.Component {
  componentDidMount () {
    const script = document.createElement("script");
    //        <script src="dist/js/demo.js"></script>
    //<script src="dist/js/pages/mydashboard.js"></script>
    script.src = "dist/js/demo.js";
    script.async = true;

    document.body.appendChild(script);
  }

    render() {
        return (
          <div className="content-wrapper">
          <div className="content-header">
            <div className="container-fluid">
              <div className="row mb-2">
                <div className="col-sm-6">
                  <h1 className="m-0">Интерфейсы</h1>
                </div>
              </div>
            </div>
          </div>
          <section className="content">
            <div className="container-fluid">
              <div className="row">
                <div className="col-lg-3 col-6">
                  <div className="small-box bg-info">
                    <div className="inner">
                      <h5>Bluetooth Device (Personal Area Network)</h5>
      
                      <p><b>ip4: </b>169.254.193.227</p>
                      <p><b>ip6: </b>169.254.193.227</p>
                      <p><b>mac: </b>38:87:d5:af:ac:25</p>
                    </div>
                    <div className="icon">
                      <i className="ion ion-bag"></i>
                    </div>
                    <a href="#" className="small-box-footer">Перейти <i className="fas fa-arrow-circle-right"></i></a>
                  </div>
                </div>
                <div className="col-lg-3 col-6">
                  <div className="small-box bg-success">
                    <div className="inner">
                      <h3>53<sup style={{fontSize : "20px"}}>%</sup></h3>
                      <p>Bounce Rate</p>
                    </div>
                    <div className="icon">
                      <i className="ion ion-stats-bars"></i>
                    </div>
                    <a href="#" className="small-box-footer">More info <i className="fas fa-arrow-circle-right"></i></a>
                  </div>
                </div>
                <div className="col-lg-3 col-6">
                  <div className="small-box bg-warning">
                    <div className="inner">
                      <h3>44</h3>
      
                      <p>User Registrations</p>
                    </div>
                    <div className="icon">
                      <i className="ion ion-person-add"></i>
                    </div>
                    <a href="#" className="small-box-footer">More info <i className="fas fa-arrow-circle-right"></i></a>
                  </div>
                </div>
                <div className="col-lg-3 col-6">
                  <div className="small-box bg-danger">
                    <div className="inner">
                      <h3>65</h3>
                      <p>Unique Visitors</p>
                    </div>
                    <div className="icon">
                      <i className="ion ion-pie-graph"></i>
                    </div>
                    <a href="#" className="small-box-footer">More info <i className="fas fa-arrow-circle-right"></i></a>
                  </div>
                </div>
              </div>
              <div className="row">
                <section className="col-lg-7 connectedSortable">
                  <div className="card">
                    <div className="card-header">
                      <h3 className="card-title">
                        Работа системы
                      </h3>
      
                    </div>
                    <div className="card-body">
                      <div className="tab-content p-0">
                        <div className="chart tab-pane active" id="revenue-chart"
                             style={{"position": "relative", "height": "300px"}}>
                            <canvas id="revenue-chart-canvas" height="300" style={{"height": "300px"}}></canvas>
                         </div>
                      </div>
                    </div>
                  </div>
      
                </section>
                <section className="col-lg-5 connectedSortable">
      
                  <div className="card">
                    <div className="card-header">
                      <h3 className="card-title">Simple Full Width Table</h3>
      
                      <div className="card-tools">
                        <ul className="pagination pagination-sm float-right">
                          <li className="page-item"><a className="page-link" href="#">«</a></li>
                          <li className="page-item"><a className="page-link" href="#">1</a></li>
                          <li className="page-item"><a className="page-link" href="#">2</a></li>
                          <li className="page-item"><a className="page-link" href="#">3</a></li>
                          <li className="page-item"><a className="page-link" href="#">»</a></li>
                        </ul>
                      </div>
                    </div>
                    <div className="card-body p-0">
                      <table className="table">
                        <thead>
                          <tr>
                            <th style={{"width": "10px"}}>#</th>
                            <th>Task</th>
                            <th>Progress</th>
                            <th style={{"width": "40px"}}>Label</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>1.</td>
                            <td>Update software</td>
                            <td>
                              <div className="progress progress-xs">
                                <div className="progress-bar progress-bar-danger" style={{"width": "55%"}}></div>
                              </div>
                            </td>
                            <td><span className="badge bg-danger">55%</span></td>
                          </tr>
                          <tr>
                            <td>2.</td>
                            <td>Clean database</td>
                            <td>
                              <div className="progress progress-xs">
                                <div className="progress-bar bg-warning" style={{"width": "70%"}}></div>
                              </div>
                            </td>
                            <td><span className="badge bg-warning">70%</span></td>
                          </tr>
                          <tr>
                            <td>3.</td>
                            <td>Cron job running</td>
                            <td>
                              <div className="progress progress-xs progress-striped active">
                                <div className="progress-bar bg-primary" style={{width : "30%"}}></div>
                              </div>
                            </td>
                            <td><span className="badge bg-primary">30%</span></td>
                          </tr>
                          <tr>
                            <td>4.</td>
                            <td>Fix and squish bugs</td>
                            <td>
                              <div className="progress progress-xs progress-striped active">
                                <div className="progress-bar bg-success" style={{width : "90%"}}></div>
                              </div>
                            </td>
                            <td><span className="badge bg-success">90%</span></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
      
                </section>
              </div>
            </div>
          </section>

        </div>)
    }
}

export default Contents