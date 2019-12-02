import React, { Component, Fragment } from 'react';
import MainFunc from './mainFunction'
import Header from './header'
import Footer from './footer'
// import data from './dataStore'

const axios = require('axios');
const url = "http://localhost:8000/Good2Know/?user_id=";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userID: "",
      topics: {
        labels : [],
        data : [],
      },
      posts: []
    };

    this.handleSend = this.handleSend.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.getPosts = this.getPosts.bind(this)
  }

  getPosts = () => {
    axios.get(url + this.state.userID)
      .then((response) => {
        // handle success
        // const titles = response.data.map(data => data.title)
        //var myObject = JSON.parse(response.data)
        console.log(response.data);
        this.setState({
          posts: response.data.posts,
          topics : {
            labels : response.data.topics.labels,
            data : response.data.topics.data,
          }
        })

      })
      .catch((error) => {
        // handle error
        console.log(error);
      })
  }

  handleSend = (event) => {
    // console.log("Send:", this.state.userID)
    this.getPosts()
  }

  handleChange = (event) => {
    // console.log('change!')
    this.setState({
      userID: event.target.value
    })
  }

  render() {
    return (
      <Fragment>
        <Header />
        <MainFunc
          userID={this.state.userID}
          handleChange={this.handleChange}
          handleSend={this.handleSend}
          posts={this.state.posts}
          topics={this.state.topics}
        />
        <Footer />
      </Fragment>
    );
  }
}

export default App;
