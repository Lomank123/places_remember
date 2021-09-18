import React, { Component } from 'react';
import ReactDOM from "react-dom";
import "../styles/leaflet-style.css";
import 'leaflet/dist/leaflet.css';
import LeafletMap from './map';


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
    // instead of getCookies
    let auth = new coreapi.auth.SessionAuthentication({
      csrfCookieName: 'csrftoken',
      csrfHeaderName: 'X-CSRFToken',
    });
    // If you have logged in previously it'll reflect the changes 
    const client = new coreapi.Client({auth: auth});

    client.action(schema, ["recollections", "read"], {'id': this.rec_id})
      .then((result) => {
        if (result["geom"] != null) {
          const rawData = JSON.parse(result["geom"]);
          const coords = rawData["coordinates"];
          this.props.handler(coords[1], coords[0]);
        } else {
          console.log("geom is null");
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