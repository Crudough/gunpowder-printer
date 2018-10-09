const mongoose = require('mongoose');
const moment = require('moment');

//Data Schema
var ImageSchema = mongoose.Schema({
	image64: String,
	timesent: Number,
	timereceieved: {
		type: Number,
		default: moment().unix()
	}
});

var Image = module.exports = mongoose.model('Image', ImageSchema);

module.exports.getImageById = (id, callback) => {
	Image.findById(id, callback);
};