import React, { Component } from 'react';
import Auth from '../Auth';

class Header extends Component {
    state = {
        user: "",
        password: "",
        isLoggedIn: false,
        successAlert: false
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

        return (
            <React.Fragment>
                <header style={headerStyle} >
                    <h1>Student Jobs</h1>
                    <Auth
                        refresh={this.props.refresh}
                        jobs={this.props.jobs}
                    />
                </header>
            </React.Fragment>
        )
    }
}

export default Header;