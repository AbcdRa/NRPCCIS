import React from 'react';
import axios from 'axios';

class MainIfaceElement extends React.Component {
  render() {
    return (
  <div className="col card-group mb-2" >
     <div className={this.props.iface.is_mon ? 'card bg-success':"card bg-info"} >
      <div className="card-body">
      
        <h4 className='text-center'><b>{this.props.iface.index}</b></h4>
        {this.props.iface.desc}
        
      </div>
      <ul className="list-group list-group-flush" style={{color:"black"}}>
          {this.props.iface.ip4.length > 0 && <li className="list-group-item"><b>ip4: </b> {this.props.iface.ip4}</li>}
          {this.props.iface.ip6.length > 0 && <li className="list-group-item"><b>ip6: </b>{this.props.iface.ip6}</li>}
          {this.props.iface.mac.length > 0 && <li className="list-group-item"><b>mac: </b>{this.props.iface.mac}</li>}
        </ul>
      <div className="icon">
        <i className="ion ion-bag"></i>
      </div>
      <a href={"/iface/"+this.props.iface.index} className="card-footer">Перейти <i className="fas fa-arrow-circle-right"></i></a>
      </div>
  </div>
    )
  }
}

class MainIfaceRow extends React.Component {
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
          <div className="content-header">
          <div className="container-fluid">
            <div className="row mb-2">
              <div className="col-sm-6">
                <h1 className="m-0">Интерфейсы</h1>
              </div>
            </div>
          </div>
        </div>
        <div className="row row-cols-6">
        {this.state.ifaces.map(el => <MainIfaceElement iface={el} key={el.desc}></MainIfaceElement>)}
        </div>
      </div>
      )
  }
}

export default MainIfaceRow