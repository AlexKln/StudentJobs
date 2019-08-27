import React, { Component } from 'react';
import JobItem from './JobItem';
import { Accordion } from 'react-bootstrap';

class Jobs extends Component {
  render() {
    return (
      <Accordion defaultActiveKey="0">
        {
          this.props.location.state.jobs.map((job) => (
            <JobItem key={job.id} job={job} />
          ))
        }
      </Accordion>
    )
  }
}

export default Jobs;
