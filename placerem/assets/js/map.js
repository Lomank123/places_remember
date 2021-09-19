import React, { Component } from 'react';
import L from 'leaflet';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import "../styles/leaflet-style.css";
import 'leaflet/dist/leaflet.css';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';


// Setting the default marker icon (default doesn't load)
let DefaultIcon = L.icon({
  iconRetinaUrl: iconRetina,
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 45],
  iconAnchor: [15, 45],
});
L.Marker.prototype.options.icon = DefaultIcon;

const pos = [0, 0];
// Need to move token to .env file
const access_token = 'pk.eyJ1IjoibG9tYW5rIiwiYSI6ImNrc2ozM285NzI5aDIyeG9kbzhnMTh1czEifQ.VbvbOjViOdSMnybzEkOgZQ';
const url = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + access_token;


export default class LeafletMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      components: this.props.components,
      marker: [],
      isDelete: false,
      isMarker: false,
    }
  }

  // Method checks whether marker exists at the moment
  isActiveMarker = () => {
    return this.state.isMarker
  }

  // Get coordinates of a present marker
  getMarkerCoords = () => {
    if (this.isActiveMarker()) {
      return this.state.marker;
    }
    return [];
  }

  // Before setting coords for a new marker the old one must be erased
  addMarker = (lat, lng, isDelete=false) => {
    if (this.isActiveMarker()) {
      this.deleteMarker();
    }
    this.setMarkerCoords(lat, lng, isDelete);
  }

  // Sets marker coords and after setState a new marker should appear on the map
  setMarkerCoords = (lat, lng, isDelete=false) => {
    const newMarker = [lat, lng];
    this.setState({marker: newMarker, isMarker: true, isDelete: isDelete});
    console.log("Marker has been added at: " + newMarker);
  }

  // Removes the present marker
  deleteMarker = () => {
    this.setState({marker: [], isMarker: false, isDelete: false});
    console.log("Marker has been removed ");
  }

  // Needed for Marker eventHandler prop, perhaps there is a better solution
  empty = () => {
    return null;
  }

  render() {
    const isMarker = this.isActiveMarker();
    const isDelete = this.state.isDelete;
    return (
      <MapContainer
        className="leaflet-new-map" 
        center={pos} 
        zoom={1}
        zoomSnap={0.25}
      >
        <TileLayer 
          url={url}
          attribution='Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'
          maxZoom={13}
          id='mapbox/streets-v11'
          tileSize={512}
          zoomOffset={-1}
        />
        {
          // Use Object.entries(dict) to pass dict to map function (by default map can serve only arrays)
          Object.entries(this.state.components).map(([key, Comp]) => {
            return (
              // Each component should have unique key
              <Comp key={key} add_marker={this.addMarker} get_coords={this.getMarkerCoords} />
            );
          })
        }
        {
          isMarker ? <Marker position={this.state.marker}
                              eventHandlers={{ click: isDelete ? this.deleteMarker : this.empty }} /> : null
        }
      </MapContainer>
    );
  }
}
