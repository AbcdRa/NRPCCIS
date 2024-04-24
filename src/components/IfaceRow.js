import React from 'react';

class IfaceElement extends React.Component {
  render() {
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
  }
}

class IfaceRow extends React.Component {
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
      <div className="row">
        <IfaceElement></IfaceElement>
      </div>
      )
  }
}

export default IfaceRow