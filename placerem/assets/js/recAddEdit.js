import React, { useEffect } from 'react';
import ReactDOM from "react-dom";
import { useMapEvents } from 'react-leaflet';
import LeafletMap from './map';
import { getClient } from './utils';

// coreapi and schema was imported from html script tag

function AddEditMapComponent (props) {
  const client = getClient(coreapi);

  const ids = JSON.parse(document.getElementById('add_info').textContent);
  const user_id = ids["user_id"];
  const rec_id = ids["rec_id"];

  const submit_btn = document.getElementById('submit_btn');
  const rec_name = document.getElementById('id_name');
  const rec_descr = document.getElementById('id_description');

  const map = useMapEvents({
    'click': (e) => {
      addMarkerOnClick(e);
    }
  });

  // Regards to this setter will work properly and save the data
  useEffect(() => {
    if (rec_id) {
      client.action(schema, ["recollections", "read"], {'id': rec_id}).then((result) => {
        if (result["geom"] != null) {
          const rawData = JSON.parse(result["geom"]);
          const coords = rawData["coordinates"];
          props.add_marker(coords[0], coords[1], true);
        }
      })
    }
    submit_btn.addEventListener("click", function() {
      sendData();
    });
  }, [])

  function addMarkerOnClick(e) {
    const { lat, lng } = e.latlng;
    props.add_marker(lat, lng, true);
  }

  function collectData() {
    var collectedData = {
      name: rec_name.value,
      description: rec_descr.value,
      user: user_id,
      geom: null
    };
    if (rec_id) {
      collectedData["id"] = rec_id; // adding id to update item
    };
    const coords = props.get_coords()
    if (coords.length != 0) {
      const point = {
        'type': 'Point',
        'coordinates': [coords[0], coords[1]],
      };
      collectedData["geom"] = JSON.stringify(point);
    };
    return collectedData;
  }

  function sendData() {
    var data = collectData();
    if (rec_id) {
      // put
      client.action(schema, ["recollections", "update"], data).then((result) => {
        console.log(result);
        console.log("put");
        window.location.href = "/home/"; // redirect must be here otherwise django data won't be updated
      });
    } else {
      // post
      client.action(schema, ["recollections", "create"], data).then((result) => {
        console.log(result);
        console.log("post");
        window.location.href = "/home/";
      });
    }
  }
  
  return null;
}


const components = {
  add_edit: AddEditMapComponent,
}

ReactDOM.render(
  <LeafletMap components={components} />,
  document.getElementById('recmap')
);