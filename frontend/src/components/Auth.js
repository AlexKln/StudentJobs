import React, { Component } from 'react';
import { Link, Redirect } from 'react-router-dom';
import Refresh from './Refresh';
import NavigationBar from './NavigationBar';
import axios from 'axios';
import { Alert, Button, FormGroup, FormLabel, FormControl, Nav } from 'react-bootstrap'

class Auth extends Component {
    state = {
        user: "",
        password: "",
        isLoggedIn: false,
        successAlert: false
    }

    componentDidMount() {
        const AuthStr = 'Bearer ' + this.getToken()
        axios.get('http://' + process.env.REACT_APP_HOST_URL + '/validate',
            { 'headers': { 'Authorization': AuthStr } })
            .then(res => this.setState({ isLoggedIn: true })
            )
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.successAlert) {
            this.turnOffSuccessAlert = setTimeout(() => {
                this.setState({ successAlert: false })
            }, 1500)
        }
    }

    componentWillUnmount() {
        clearTimeout(this.turnOffSuccessAlert);
        clearTimeout(this.turnOffFailureAlert);
    }

    setToken = idToken => {
        // Saves user token to localStorage
        localStorage.setItem("id_token", idToken)
    }

    getToken = () => {
        // Retrieves the user token from localStorage
        return localStorage.getItem("id_token")
    }

    handleChange = (event) => {
        const { name, value } = event.target
        this.setState({ [name]: value })
    }

    handleSubmit = (event) => {
        event.preventDefault();

        axios.post('http://' + process.env.REACT_APP_HOST_URL + '/login', {
            username: this.state.user,
            password: this.state.password
        })
            .then(res => {
                this.setToken(res.data.access_token)
                this.setState(prevState => {
                    prevState.successAlert = true
                    prevState.isLoggedIn = true
                    return prevState
                }
                )
            }
            ).catch(
                error => {
                    try {
                        alert(error.response.data.message)
                    }
                    catch (err) {
                        alert('Something went wrong')
                    }
                }
            )
        // .catch(function (error) {
        //     error.response &&
        //         console.log(error.response.status)
        // })
        setTimeout(() => !this.state.isLoggedIn && this.setState({ failureAlert: true }), 100)
    }

    logOut = (event) => {
        localStorage.removeItem("id_token")
        this.setState({
            user: "",
            password: "",
            isLoggedIn: false
        })
    }

    render() {
        const loggedIn = () => {
            return (
                <React.Fragment>
                    <NavigationBar 
                    jobs={this.props.jobs}
                    logOut={this.logOut}
                    />
                    {this.state.successAlert && <Alert
                        key={1}
                        variant="success"
                    >
                        Success!
                    </Alert>}
                    <p />
                    <Refresh refresh={this.props.refresh} />
                    <Redirect
                        to={{
                            pathname: "/jobs",
                            state: { jobs: this.props.jobs }
                        }}
                    />
                </React.Fragment>
            )
        }

        const loggedOut = () => {
            return (
                <div className="Login">
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
                            Login
                        </Button>
                        <Nav.Link as={Link} to='/register'>
                            Register
                        </Nav.Link>
                    </form>
                    <Redirect to='/' />
                </div>
            )
        }

        return (
            this.state.isLoggedIn ? loggedIn() : loggedOut()
        )
    }
}

export default Auth;