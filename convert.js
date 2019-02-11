const express = require("express");
const Image = require("./schema.js");

exports.post_api = (req, res, next) => {
  var { image64 } = req.body;

  // req.checkBody("image64", "Please select an image.").notEmpty();
  // req.checkBody("timesent", "Invalid time code receieved.").isNumeric();
  //req.checkBody('timesent', 'No time code received.').isEmpty();
  var errors = req.validationErrors();
  if (errors) {
    res.status(404).send({ message: errors });
  } else {
    var newImage = new Image({
      image64: image64,
      timesent: new Date().getTime()
    });

    newImage.save();

    var spawn = require("child_process").spawn,
      python = spawn("python", ["Python Pipeline/image_processing.py"]);
    (data = newImage.image64), (dataString = "");

    python.stdout.on("data", function(data) {
      dataString += data.toString();
    });
    python.stdin.end();

    res.status(200).send(newImage);
    console.log("WE GOT HERE");
  }
};

exports.get_all_api = (req, res, next) => {
  Image.find({}, (err, result) => {
    if (err) {
      res.status(404).send({ message: "An error has occured.", err: err });
    } else {
      res.status(200).send(result);
    }
  });
};
