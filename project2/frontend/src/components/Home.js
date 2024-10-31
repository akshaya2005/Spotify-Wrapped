import React, { Component } from "react";
import {
  Grid,
  Button,
  Typography,
  responsiveFontSizes,
} from "@material-ui/core";
export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      spotifyAuthenticated: false,
    };

    this.authenticateSpotify = this.authenticateSpotify.bind(this);

  }

authenticateSpotify()
{
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        console.log(data.status);
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
    }
}