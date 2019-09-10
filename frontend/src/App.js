import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Jobs from './components/Jobs';
// import Refresh from './components/Refresh';
import About from './components/pages/About';
import Register from './components/pages/Register';
// import uuid from 'uuid';
import axios from 'axios';
import { Alert } from 'react-bootstrap'
import './App.css';

class App extends Component {
  state = {
    jobs: []
  }

  componentDidMount() {
    axios.get('http://' + process.env.REACT_APP_HOST_URL + '/').then(res => this.setState({ jobs: res.data }))
  }

  // refresh
  refresh = (title) => {
    axios.post('https://tobe.implemented', {
      title,
      completed: false
    })
      .then(res => this.setState({ jobs: [...this.state.jobs, res.data] }));
  }

  render() {
    const alertStyle = {
      fontSize: '17px'
    }

    return (
      <Router>
        <div className="App">
          <div className="container-fluid">
            <Header
              refresh={this.refresh}
              jobs={this.state.jobs}
            />
            <Route exact path="/" render={props => (
              <React.Fragment>
                <center>
                  <Alert
                    key={1}
                    variant="primary"
                  >
                    <span style={alertStyle}>
                      Log in or register to display jobs please
                    </span>
                  </Alert>
                </center>
                {/* <Refresh refresh = {this.refresh}/>
            <Jobs jobs={this.state.jobs}/> */}
              </React.Fragment>
            )} />
            <Route path="/jobs" component={Jobs} />
            <Route path="/about" component={About} />
            <Route path="/register" component={Register} />
          </div>
        </div>
      </Router>
    );
  }
}

export default App;