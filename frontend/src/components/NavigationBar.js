import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Button, Navbar, Nav } from 'react-bootstrap'

class NavigationBar extends Component {
    state = {

    }

    render() {

        return (
            <React.Fragment>
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
                    <Button variant="outline-danger" onClick={this.props.logOut}>Log Out</Button>
                </Navbar>
            </React.Fragment>
        )
    }
}

export default NavigationBar