import React, { Component } from "react";
//import Button from "@material-ui/core/Button";
import "./App.css";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
//import IconButton from "@material-ui/core/IconButton";
import Icon from "@material-ui/core/Icon";
import axios from "axios";

class App extends Component {
  constructor() {
    super();
    this.state = {
      upload: false,
      //connected: false,
      image: null,
      converted_image: null
    };
  }

  handleChange = event => {
    this.compress(event.target.files[0]);
    let reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    reader.onload = e => {
      //this.getDataUrl(e.target.result);
      this.setState({ image: e.target.result });
    };

    this.setState({ upload: true });

    //this.compress(this.image);
  };

  compress(e) {
    const fileName = e.name;
    let reader = new FileReader();
    reader.readAsDataURL(e);
    reader.onload = event => {
      const img = new Image();
      img.src = event.target.result;
      img.onload = () => {
        const elem = document.createElement("canvas");
        elem.width = 125;
        elem.height = 125;
        const ctx = elem.getContext("2d");
        // img.width and img.height will contain the original dimensions
        ctx.drawImage(img, 0, 0, 125, 125);
        ctx.canvas.toBlob(
          blob => {
            const file = new File([blob], fileName, {
              type: "image/png",
              lastModified: Date.now()
            });
            let newReader = new FileReader();
            newReader.readAsDataURL(file);
            newReader.onload = newFile => {
              this.getDataUrl(newFile.target.result);
            };
          },
          "image/png",
          1
        );
      };
    };
  }

  getDataUrl = url => {
    const base = url.replace(/^data:image\/(png|jpg);base64,/, "");
    console.log("New File Base 64: ", base);
    try {
      axios
        .post("http://localhost:3001/convert", {
          image64: base
        })
        .then(response => {
          console.log(response);
          this.setState({ converted_image: response });
        })
        .catch(error => {
          console.log(error);
        });
    } catch (error) {
      console.log(error);
    }
  };

  render() {
    const { upload, image } = this.state;

    return (
      <div className="App">
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" color="inherit" style={{ flexGrow: 1 }}>
              Welcome to the Gunpowder Printer!
            </Typography>
            {/* <IconButton
              style={{
                marginLeft: -12,
                marginRight: 20
              }}
              onClick={() =>
                this.setState(prev => ({ connected: !prev.connected }))
              }
              color="inherit"
              aria-label="Menu"
            >
              <Icon>{connected ? "wifi_off" : "wifi"}</Icon>
            </IconButton> */}
          </Toolbar>
        </AppBar>
        <header className="App-header">
          {upload ? (
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center"
              }}
            >
              <div
                style={{
                  backgroundColor: "white",
                  borderRadius: 4,
                  height: 500,
                  width: 500,
                  boxShadow: "0px 2px 5px 0px rgba(0,0,0,0.5)",
                  margin: 10,
                  backgroundImage: `url(${image})`,
                  backgroundSize: "500px 500px",
                  backgroundRepeat: "no-repeat",
                  backgroundPosition: "center"
                }}
              />
              {/* <Icon color="primary">arrow_forward_ios</Icon>
              <div
                style={{
                  // backgroundImage: `url(${this.state.converted_image})`,
                  backgroundColor: "white",
                  borderRadius: 4,
                  height: 125,
                  width: 125,
                  boxShadow: "0px 2px 5px 0px rgba(0,0,0,0.5)",
                  margin: 10
                }}
              >
                <img
                  src={this.state.converted_image}
                  alt="new pic"
                  style={{ width: "100%", height: "90%" }}
                />
              </div> */}
            </div>
          ) : null}
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              alignItems: "center",
              width: "75%"
            }}
          >
            <input
              type="file"
              id="picker"
              style={{ display: "none  " }}
              onChange={this.handleChange}
            />
            <label
              htmlFor="picker"
              style={{
                fontFamily: "Arial",
                border: "none",
                borderRadius: 4,
                backgroundColor: upload ? "purple" : "#3e4ebc",
                margin: 10,
                padding: 10,
                cursor: "pointer"
              }}
            >
              {upload ? "New Image" : "Upload"}
              <Icon style={{ marginLeft: 10 }}> cloud_upload</Icon>
            </label>
            {/* <Button
              variant="contained"
              color={upload ? "secondary" : "primary"}
              style={{
                margin: 10
              }}
              //onClick={() => this.setState(prev => ({ upload: !prev.upload }))}
            >
              
              
            </Button> */}
            {/* {upload ? (
              <Button
                variant="contained"
                color="primary"
                style={{
                  margin: 10
                }}
                onClick={() => this.setState({ print: true })}
              >
                Print
                <Icon style={{ marginLeft: 10 }}> print</Icon>
              </Button>
            ) : null} */}
          </div>
        </header>
      </div>
    );
  }
}

export default App;
