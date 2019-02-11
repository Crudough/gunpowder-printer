const express = require("express");
const bodyParser = require("body-parser");
const expressValidator = require("express-validator");
const convert = require("./convert");
const mongo = require("mongodb");
const mongoose = require("mongoose");
const cors = require("cors");

// Initialize the App.
const app = express();
app.use(cors());

app.use((res, req, next) => {
  res.header("Access-Control-All-Origin", "*");
  res.header(
    "Access-Control-Methods",
    "PUT",
    "POST",
    "GET",
    "PATCH",
    "DELETE",
    "OPTIONS"
  );
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested_with, Content-Type, Accept, Authorization"
  );
  next();
});
//Initialize Database
var mongoConnection = {
  url: "mongodb://127.0.0.1/gunpowder-printer"
};

mongoose
  .connect(mongoConnection.url)
  .then(() => {
    console.log("Connection to database is complete.");
  })
  .catch(err => {
    console.error("Something wwent wrong :/", err.stack);
  });
// Middleware
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ limit: "50mb", extended: false }));

// app.use(
//   expressValidator({
//     errorFormatter: function(param, msg, value) {
//       var namespace = param.split("."),
//         root = namespace.shift(),
//         formParam = root;

//       while (namespace.length) {
//         formParam += "[" + namespace.shift() + "]";
//       }
//       return {
//         param: formParam,
//         msg: msg,
//         value: value
//       };
//     }
//   })
// );

//localhost:3001/
app.use("/convert", convert);

//GET and POST Requests
app.get("/", (req, res) => res.send("Hello World!"));
// app.post("/convert", convert.post_api);
// app.get("/get_images", convert.get_all_api);

//Port setup.
app.set("port", process.env.PORT || 3001);

//Open ears
app.listen(app.get("port"), function() {
  console.log("Server started on port " + app.get("port"));
});
