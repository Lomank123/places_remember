import React, { Component } from 'react';
import ReactDOM from "react-dom";
import LeafletMap from './map';
import { getClient } from './utils';


class DetailMapComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {}
    const ids = JSON.parse(document.getElementById('add_info').textContent);
    this.user_id = ids["user_id"];
    this.rec_id = ids["rec_id"];
    this.getData()
  }

  // Fetches data from api (single recollection)
  getData() {
    const client = getClient(coreapi);
    client.action(schema, ["recollections", "read"], {'id': this.rec_id})
      .then((result) => {
        if (result["geom"] != null) {
          const rawData = JSON.parse(result["geom"]);
          const coords = rawData["coordinates"];
          this.props.add_marker(coords[0], coords[1]);
        }
      })
  }

  render() {
    return(null);
  }
}


const components = {
  detail: DetailMapComponent,
}

ReactDOM.render(
  <LeafletMap components={components} />,
  document.getElementById('recmap')
);