var last_chosen_event = 'Basic Event 1'
var last_chosen_metric = 'Reliability'

$(document).ready(function(){
    $("input:radio[name=events]").click(function() {
        var event = $(this).val();
        last_chosen_event = event
        document.getElementById("event_title").innerHTML = event;
        var metric = last_chosen_metric;
        //console.log(metric);
        var image_name = event.toLowerCase().replace(/ /g,"_");
        var directory = '/static/images/';
        var png = '.png';
        var source = directory.concat(image_name.concat('_'.concat(metric.concat(png))));
        //console.log(source);
        $('#plot').attr('src', source);
    });
});
$(document).ready(function(){
    $("input:radio[name=metric]").click(function() {
        var metric = $(this).val();
        last_chosen_metric = metric;
        var event = last_chosen_event;
        //console.log(event);
        var image_name = event.toLowerCase().replace(/ /g,"_");
        var directory = '/static/images/';
        var png = '.png';
        var source = directory.concat(image_name.concat('_'.concat(metric.concat(png))));
        //console.log(source);
        $('#plot').attr('src', source);
    });
});
