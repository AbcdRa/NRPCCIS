import React from 'react';
import MainIfaceRow from './MainIfaceRow';
import Others from './Others';



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
          <section className="content">
            <div className="container-fluid">
              <MainIfaceRow></MainIfaceRow>
            </div>
          </section>
        </div>)
    }
}

export default Contents