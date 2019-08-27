import React, { Component } from 'react';
import { Link, Redirect } from 'react-router-dom';
import Refresh from '../Refresh';
import axios from 'axios';
import { Alert, Button, FormGroup, FormLabel, FormControl, Navbar, Nav } from 'react-bootstrap'

class Header extends Component {
    state = {
        user: "",
        password: "",
        isLoggedIn: false,
        successAlert: false
    }

    componentDidMount() {
        const AuthStr = 'Bearer ' + this.getToken();
        axios.get('http://127.0.0.1:5000/validate', { 'headers': { 'Authorization': AuthStr } }).then(res => this.setState({ isLoggedIn: true }))
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
        // (this.state.user === 'admin' && this.state.password === 'admin')
        //     &&
        //     this.setState(prevState => {
        //         prevState.successAlert = true
        //         prevState.isLoggedIn = true
        //         return prevState
        //     })
        axios.post('http://127.0.0.1:5000/login', {
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
        const headerStyle = {
            background: '#333',
            color: '#fff',
            textAlign: 'center',
            padding: '10px'
        }

        // const linkStyle = {
        //     color: '#fff',
        //     textDecoration: 'none'
        // }

        const loggedIn = () => {
            return (
                <React.Fragment>
                    <header style={headerStyle} >
                        <h1>Student Jobs</h1>
                        <Navbar bg="light" expand="lg">
                            <Navbar.Toggle aria-controls="basic-navbar-nav" />
                            <Navbar.Collapse id="basic-navbar-nav">
                                <Nav className="mr-auto">
                                    <Nav.Link as={Link} to={{
                                        pathname: "/jobs",
                                        state: { jobs: this.props.jobs }
                                    }}>Home</Nav.Link>
                                    <Nav.Link as={Link} to="/about">About</Nav.Link>
                                </Nav>
                            </Navbar.Collapse>
                            <Button variant="outline-danger" onClick={this.logOut}>Log Out</Button>
                        </Navbar>
                        {this.state.successAlert && <Alert
                            key={1}
                            variant="success"
                        >
                            Success!
                    </Alert>}
                    </header>
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
                <React.Fragment>
                    <header style={headerStyle} >
                        <h1>Student Jobs</h1>
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
                        </div>
                    </header>
                    {/* <Refresh refresh = {this.props.refresh}/> */}
                    <Redirect to='/' />
                </React.Fragment>
            )
        }

        return (
            this.state.isLoggedIn ? loggedIn() : loggedOut()
        )
    }
}

export default Header;