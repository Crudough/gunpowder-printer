const express = require('express');
const Image = require('./schema.js');
const fs = require('fs');
const util = require('util')

exports.post_api = (req, res, next) => {
	var {
		image64,
		timesent
	} = req.body;

	req.checkBody('image64', 'Please select an image.').notEmpty();
	req.checkBody('timesent', 'Invalid time code receieved.').isNumeric();
	//req.checkBody('timesent', 'No time code received.').isEmpty();
	var errors = req.validationErrors();
	if (errors) {
		res.status(404).send({ message : errors });
	}
	else {
		var newImage = new Image({
			image64: image64,
			timesent: timesent
		});

		newImage.save();

		res.status(200).send(newImage)
		let writeData = JSON.stringify(newImage);
		fs.writeFileSync('exported.json', writeData);
		var spawn = require('child_process').spawn;
		var python = spawn('python3', ['Python\\ Pipeline/image_processing.py']);

		util.log('Reading Python Feedback')

		process.stdout.on('data',function(chunk){

		    var textChunk = chunk.toString('utf8');// buffer to string

		    util.log(textChunk);
		});

		data = newImage.image64,
		dataString = '';
		console.log("WE GOT HERE");
	}

};

exports.get_all_api = (req, res, next) => {
	Image.find({}, (err, result) => {
		if (err) {
			res.status(404).send({ message: 'An error has occured.', err : err });
		}
		else {
			res.status(200).send(result);
		}
	});
}
