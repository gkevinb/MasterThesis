var last_chosen_event = 'Basic Event 1'
var last_chosen_metric = 'Reliability'
var original_fault_tree
var reconstructed_fault_tree


function EventRadioButtonListener(){
    $(document).ready(function(){
        $("input:radio[name=events]").click(function() {
            var event = $(this).val();
            last_chosen_event = event
            document.getElementById("event_title").innerHTML = event;
            var metric = last_chosen_metric;
            var image_name = event.toLowerCase().replace(/ /g,"_");
            var directory = '/static/images/';
            var png = '.png';
            var source = directory.concat(image_name.concat('_'.concat(metric.concat(png))));
            $('#plot').attr('src', source);
        });
    });
}

function MetricRadioButtonListener(){
    $(document).ready(function(){
        $("input:radio[name=metric]").click(function() {
            var metric = $(this).val();
            last_chosen_metric = metric;
            var event = last_chosen_event;
            var image_name = event.toLowerCase().replace(/ /g,"_");
            var directory = '/static/images/';
            var png = '.png';
            var source = directory.concat(image_name.concat('_'.concat(metric.concat(png))));
            $('#plot').attr('src', source);
        });
    });
}

function init(){
    EventRadioButtonListener()
    MetricRadioButtonListener()
}
$.getJSON('/static/data.json', function(data){
    original_fault_tree = data.OriginalFaultTree
    reconstructed_fault_tree = data.ReconstructedFaultTree
    init();
});
/*
function fillEventInformation(event) {
    if (event == 'top_event') {
        document.getElementById("oft_rel_dis").innerHTML = original_fault_tree.;
        document.getElementById("rft_rel_dis").innerHTML = original_fault_tree.name;
        document.getElementById("oft_main_dis").innerHTML = original_fault_tree.length));
        document.getElementById("rft_main_dis").innerHTML = formatArea(sf2sm(wall_database[index].area));
        document.getElementById("oft_mtbf").innerHTML = formatVolume(cf2cm(wall_database[index].volume));
        document.getElementById("rft_mtbf").innerHTML = wall_database[index].completeness;
        document.getElementById("oft_mtbr").innerHTML = formatCost(wall_database[index].cost_so_far);
        document.getElementById("rft_mtbr").innerHTML = formatVolume(cf2cm(wall_database[index].volume));

        document.getElementById("oper_avail").innerHTML = formatCost(wall_database[index].cost_so_far);
    }
}
*/