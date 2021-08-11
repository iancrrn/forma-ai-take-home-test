/* Forma AI take-home test by Ian Carreon, iancrrn@gmail.com, 26 May 2020 */

import React from 'react';
import PropTypes from 'prop-types';
import Card from './Card';
import Graph from './Graph';

const { arrayOf, shape } = PropTypes;

const RevenueGraphView = (props) => {
  return ( <div>
             <Graph data={props.data} />
           </div>
  )
};

RevenueGraphView.propTypes = {
  data: arrayOf(shape()),
};

export default RevenueGraphView;
