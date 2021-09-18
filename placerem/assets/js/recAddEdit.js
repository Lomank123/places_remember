import React, { useEffect, useState, useRef } from 'react';
import ReactDOM from "react-dom";
import L from 'leaflet';
import { useMapEvents } from 'react-leaflet';
import "../styles/leaflet-style.css";
import 'leaflet/dist/leaflet.css';
import LeafletMap from './map';


const coreapi = window.coreapi;
const schema = window.schema;

function AddEditComponent (props) {
  const [loadedMarker, setLoadedMarker] = useState(null);
  const marker = useRef(null);
  const isFirstRender = useRef(true);

  // instead of getCookies
  let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken',
  });
  // If you have logged in previously it'll reflect the changes 
  const client = new coreapi.Client({auth: auth});

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
        setLoadedMarker(result);
      });
    }
    submit_btn.addEventListener("click", function() {
      sendData();
    });
  }, [])

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
    } else {
      const loadedRecGeom = JSON.parse(loadedMarker["geom"]);
      // If marker existed (geom != null)
      if (loadedRecGeom != null) {
        // first: lng, second: lat
        const coords = loadedRecGeom["coordinates"];
        var lat = coords[1];
        var lng = coords[0];
        createMarker(lat, lng);
      }
    }
  }, [loadedMarker])

  function addMarkerOnClick(e) {
    if (marker.current != null) {
      removeMarker();
    }
    const { lat, lng } = e.latlng;
    createMarker(lat, lng);
  }

  function createMarker(lat, lng) {
    marker.current = L.marker([lat, lng]).addTo(map);
    marker.current.on("click", function() {
      removeMarker();
      console.log("Marker removed");
    });
    console.log("Marker placed on: " + marker.current._latlng);
  }
  
  function removeMarker() {
    map.removeLayer(marker.current);
    marker.current = null;
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
    if (marker.current != null) {
      const point = {
        'type': 'Point',
        'coordinates': [marker.current._latlng["lng"], marker.current._latlng["lat"]]
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


// This is how the output should look like
const components = {
  add_edit: AddEditComponent,
}

ReactDOM.render(
  <LeafletMap components={components} />,
  document.getElementById('recmap')
);