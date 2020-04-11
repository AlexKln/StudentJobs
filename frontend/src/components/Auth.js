import React, { useState, useEffect } from 'react'
import { Link, Redirect } from 'react-router-dom';
import Refresh from './Refresh';
import NavigationBar from './NavigationBar';
import axios from 'axios';
import { Alert, Button, FormGroup, FormLabel, FormControl, Nav } from 'react-bootstrap'

function Auth(props) {
    const [user, setUser] = useState("")
    const [password, setPassword] = useState("")
    const [loggedIn, setLoggedIn] = useState(false)
    const [successAlert, setSuccessAlert] = useState(false)

    useEffect(() => {
        const AuthStr = 'Bearer ' + getToken()
        axios.get('http://' + process.env.REACT_APP_HOST_URL + '/validate',
            { 'headers': { 'Authorization': AuthStr } })
            .then(res => setLoggedIn(true))
    }, [])

    useEffect(() => {
        if (successAlert) {
            setTimeout(() => {
                setSuccessAlert(false)
            }, 1500)
        }
    }, [successAlert])

    function setToken(idToken) {
        // Saves user token to localStorage
        localStorage.setItem("id_token", idToken)
    }

    function getToken() {
        // Retrieves the user token from localStorage
        return localStorage.getItem("id_token")
    }

    function handleSubmit(event) {
        event.preventDefault();
        axios.post('http://' + process.env.REACT_APP_HOST_URL + '/login', {
            username: user,
            password: password
        })
            .then(res => {
                setToken(res.data.access_token)
                setSuccessAlert(true)
                setLoggedIn(true)
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
        setTimeout(() => !loggedIn, 100)
    }

    function logOut(event) {
        localStorage.removeItem("id_token")
        setUser("")
        setPassword("")
        setLoggedIn(false)
    }

    return (<React.Fragment>
        {loggedIn ? <React.Fragment>
            <NavigationBar
                jobs={props.jobs}
                logOut={logOut}
            />
            {successAlert ? <Alert
                key={1}
                variant="success"
            >
                Success!
                    </Alert> : null}
            <p />
            <Refresh refresh={props.refresh} />
            <Redirect
                to={{
                    pathname: "/jobs",
                    state: { jobs: props.jobs }
                }}
            />
        </React.Fragment> : <div className="Login">
                <form onSubmit={handleSubmit}>
                    <FormGroup controlId="usedr" bssize="large">
                        <FormLabel>Username</FormLabel>
                        <FormControl
                            autoFocus
                            type="text"
                            name="user"
                            value={user}
                            onChange={(e) => setUser(e.target.value)}
                        />
                    </FormGroup>
                    <FormGroup controlId="password" bssize="large">
                        <FormLabel>Password</FormLabel>
                        <FormControl
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
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
            </div>}
    </React.Fragment>)
}
export default Auth;