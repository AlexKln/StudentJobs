import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { Button, ButtonToolbar } from 'react-bootstrap'

// Feature to be implemented in the future - job adding by users

export class Refresh extends Component {
    state = {
        title: ''
    }

    onSubmit = (e) => {
        e.preventDefault();
        window.location.reload()
        // this.props.refresh(this.state.title);
        // this.setState({ title: '' });
    }

    // onChange = (e) => this.setState({
    //     [e.target.name]:
    //         e.target.value
    // });

    render() {
        return (
            <form onSubmit={this.onSubmit}>
                <ButtonToolbar>
                    <Button
                        variant="primary"
                        size="lg"
                        type="submit"
                        value="Refresh"
                        block
                    >
                        Refresh
                    </Button>
                </ButtonToolbar>
            </form>
        )
    }
}

// PropTypes
Refresh.propTypes = {
    refresh: PropTypes.func.isRequired
}

export default Refresh
