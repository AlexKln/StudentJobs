import React, { Component } from "react"
import axios from 'axios'
import { Button, FormGroup, FormLabel, FormControl } from 'react-bootstrap'

class Register extends Component {

  state = {
    user: "",
    password: "",
    registered: false
  }

  setToken = idToken => {
    // Saves user token to localStorage
    localStorage.setItem("id_token", idToken)
  }

  handleChange = (event) => {
    const { name, value } = event.target
    this.setState({ [name]: value })
  }

  handleSubmit = (event) => {
    event.preventDefault()
    axios.post('http://' + process.env.REACT_APP_HOST_URL + '/register', {
      username: this.state.user,
      password: this.state.password
    })
      .then(
        res => {
          this.setToken(res.data.access_token)
          alert('Registered successfully')
          this.setState({ registered: true })
        }
      ).catch(
        error => {
          alert(error.response.data.message)
        }
      )
  }

  render() {
    return (
      this.state.registered ? 
      window.location.reload()
      : 
      <div className="Login">
        <br />
        <form onSubmit={this.handleSubmit}>
          <FormGroup controlId="usedr" bssize="large">
            <FormLabel>Username</FormLabel>
            <FormControl
              autoFocus
              type="text"
              name="user"
              value={this.state.user}
              onChange={this.handleChange}
            />
          </FormGroup>
          <FormGroup controlId="password" bssize="large">
            <FormLabel>Password</FormLabel>
            <FormControl
              value={this.state.password}
              onChange={this.handleChange}
              type="text"
              name="password"
            />
          </FormGroup>
          <Button
            block
            bsize="large"
            type="submit"
          >
            Register
          </Button>

        </form>
      </div>
    )
  }

}
export default Register