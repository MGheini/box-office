// This event is triggered when the star rating is modified or changed
// This event also allows you to access these parameters
// value: the selected rating value
// caption: the caption for the selected rating
$('#inputRate').on('rating.change', function(event, value, caption) {
    console.log(value);
    console.log(caption);
    // we'll use this for saving rate and ...
});