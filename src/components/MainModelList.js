import React from 'react';
import axios from 'axios';


class MainModelItem extends React.Component {

    state = {
        reload: false
    };
    
    refreshPage = () => {
    this.setState(
        {reload: true},
        () => this.setState({reload: false})
    )
    }

    setModel(model_name) {
        axios.get(`http://127.0.0.1:7778/set_model?model_name=`+model_name)
        .then(res => {
            const models = res.data;
            this.setState({ models });
            this.props.update_cb()
        })
    }

    render() {
        return (
        <div className={this.props.current ? "info-box mb-3 bg-success" : "info-box mb-3 bg-warning"}>
            <span className="info-box-icon"><i className="fas fa-tag"></i></span>
            <div className="info-box-content">
            <span className="info-box-text "><h2>{this.props.model_name}</h2></span>
            <span className="info-box-number">
            {this.props.current ? 
                '' : 
                <button className='btn btn-block bg-gradient-primary btn-flat' onClick={()=>{this.setModel(this.props.model_name)}}>Выбрать</button> }
            </span>
            </div>
        </div>)
    }
}


export default class MainModelList extends React.Component {
    state = {models:[], current_model:''}

    stateUpdate() {
        axios.get(`http://127.0.0.1:7778/get_models`)
        .then(res => {
            const models = res.data;
            this.setState({ models });
        })
        axios.get(`http://127.0.0.1:7778/get_current_model`)
        .then(res => {
            const current_model = res.data;
            this.setState({ current_model });
        })
    }

    componentDidMount() {
        this.stateUpdate()
    }

    render() {
        return (
        <div>
        <div className="content-header">
            <div className="container-fluid">
                <div className="row mb-2">
                    <div className="col-sm-6">
                        <h1 className="m-0">Модели</h1>
                    </div>
                </div>
            </div>
        </div>
        <div className='col-md-4 mt-2'>
            {this.state.models.map(el => <MainModelItem current={el===this.state.current_model} model_name={el} key={el} update_cb={()=>{this.stateUpdate()}}></MainModelItem>)}
        </div>
        </div>
        )
    }
}
  