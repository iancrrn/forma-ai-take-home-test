/* Forma AI take-home test by Ian Carreon, iancrrn@gmail.com, 26 May 2020 */

import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import RevenueGraphView from '../Components/RevenueGraph';
import { loadRevenueData } from '../actions';

const { arrayOf, shape } = PropTypes;

class RevenueGraph extends React.Component {
  
  componentDidMount() {
    loadRevenueData(this.props.userId)(this.props.dispatch, this.props.getState);
  }

  render() {
    return (
      <RevenueGraphView data={this.props.revenue[this.props.userId]} />
    );
  }
}

const mapStateToProps = state => ({
  revenue: state.revenue,
});

RevenueGraph.propTypes = {
  revenue: arrayOf(shape()),
};

export default connect(mapStateToProps)(RevenueGraph);

