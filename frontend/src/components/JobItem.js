import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Card, Accordion, Button } from 'react-bootstrap';

export class JobItem extends Component {
  getStyle = () => {
    return {
      background: '#f4f4f4',
      padding: '7px',
      borderBottom: '2px #ccc dotted',
    }
  }

  render() {
    const btnStyle = {
      color: '#000000',
      padding: '3px',
      fontSize: '17px'
    }
    const contentStyle = {
      fontSize: '15px'
    }
    const { id, company, title, description, link, location } = this.props.job;
    return (
      <Card>
        <Card.Header>
          <Accordion.Toggle as={Button} style={btnStyle} variant="link" eventKey={id}>
            {title} - <b>{company}</b>, {location}
          </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={id}>
          <div className="clearfix">
            <Card.Body style={contentStyle}>
              {/* <a href={link}>Apply<br /><br /></a> */}
              <Button variant="primary" href={link}>Apply</Button><br /><br />
              <div
                // dir={ description[55] == 'פ' ? "rtl" : "ltr" } logic of switching text direction
                dangerouslySetInnerHTML={{ __html: description }}>
              </div>
            </Card.Body>
          </div>
        </Accordion.Collapse>
      </Card>
    )
  }
}

// PropTypes
JobItem.propTypes = {
  job: PropTypes.object.isRequired
}

export default JobItem