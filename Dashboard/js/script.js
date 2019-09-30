var last_chosen_event = 'Basic Event 1';
var last_chosen_metric = 'Reliability';
var original_fault_tree;
var reconstructed_fault_tree;
var timeout;

var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    }
})


function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

function formatDistribution(distribution) {
    if (distribution[0] == 'EXP') {
        var lambda = round(distribution[1], 5);
        return 'Exp(&lambda; = '.concat(lambda).concat(')');
    }
    if (distribution[0] == 'WEIBULL') {
        scale = round(distribution[1], 5);
        shape = round(distribution[2], 5);
        return 'Weibull(&alpha; = '.concat(scale).concat(', &beta; = ').concat(shape).concat(')');
    }
    if (distribution[0] == 'NORMAL') {
        mu = round(distribution[1], 5);
        sigma = round(distribution[2], 5);
        return 'Normal(&mu; = '.concat(mu).concat(', &sigma; = ').concat(sigma).concat(')');
    }
    if (distribution[0] == 'LOGNORM') {
        mu = round(distribution[1], 5);
        sigma = round(distribution[2], 5);
        return 'Lognormal(&mu; = '.concat(mu).concat(', &sigma; = ').concat(sigma).concat(')');
    }
    if (distribution[0] == 'UNIDENTIFIED DISTRIBUTION') {
        return 'N/A';
    }
}

function getBasicEventNumber(basicEventName) {
    var id = basicEventName.slice(12, basicEventName.length);
    return id
}

function EventRadioButtonListener() {
    $(document).ready(function () {
        $("input:radio[name=events]").click(function () {
            var event = $(this).val();
            last_chosen_event = event
            fillEventInformation(event)
            document.getElementById("event_title").innerHTML = event;
            var metric = last_chosen_metric;
            var image_name = event.toLowerCase().replace(/ /g, "_");
            var directory = '/MasterThesis/static/images/';
            var png = '.png';
            var source = directory.concat(image_name.concat('_'.concat(metric.concat(png))));
            $('#plot').attr('src', source);
        });
    });
}

function MetricRadioButtonListener() {
    $(document).ready(function () {
        $("input:radio[name=metric]").click(function () {
            console.log("metric radio button listener")
            var metric = $(this).val();
            last_chosen_metric = metric;
            var event = last_chosen_event;
            var image_name = event.toLowerCase().replace(/ /g, "_");
            var directory = '/MasterThesis/static/images/';
            var png = '.png';
            var source = directory.concat(image_name.concat('_'.concat(metric.concat(png))));
            console.log(source)
            $('#plot').attr('src', source);
        });
    });
}

function init() {
    EventRadioButtonListener();
    MetricRadioButtonListener();
}
$.getJSON('MasterThesis/static/data.json', function (data) {
    original_fault_tree = data.OriginalFaultTree;
    reconstructed_fault_tree = data.ReconstructedFaultTree;
    init();
});

function fillEventInformation(event) {
    if (event == 'Top Event') {
        document.getElementById("oft_rel_dis").innerHTML = "";
        document.getElementById("rft_rel_dis").innerHTML = "";
        document.getElementById("oft_main_dis").innerHTML = "";
        document.getElementById("rft_main_dis").innerHTML = "";
        document.getElementById("oft_mtbf").innerHTML = "";
        document.getElementById("rft_mtbf").innerHTML = round(reconstructed_fault_tree[0].mtbf, 5);
        document.getElementById("oft_mtbr").innerHTML = "";
        document.getElementById("rft_mtbr").innerHTML = round(reconstructed_fault_tree[0].mtbr, 5);
        oper_avail_string = round(reconstructed_fault_tree[0].oper_avail * 100, 5).toString();
        document.getElementById("oper_avail").innerHTML = oper_avail_string.concat(' %');
    } else {
        basicEventID = getBasicEventNumber(event);
        document.getElementById("oft_rel_dis").innerHTML = formatDistribution(original_fault_tree[basicEventID].reliability);
        document.getElementById("rft_rel_dis").innerHTML = formatDistribution(reconstructed_fault_tree[basicEventID].reliability);
        document.getElementById("oft_main_dis").innerHTML = formatDistribution(original_fault_tree[basicEventID].maintainability);
        document.getElementById("rft_main_dis").innerHTML = formatDistribution(reconstructed_fault_tree[basicEventID].maintainability);
        document.getElementById("oft_mtbf").innerHTML = round(original_fault_tree[basicEventID].mtbf, 5);
        document.getElementById("rft_mtbf").innerHTML = round(reconstructed_fault_tree[basicEventID].mtbf, 5);
        document.getElementById("oft_mtbr").innerHTML = round(original_fault_tree[basicEventID].mtbr, 5);
        document.getElementById("rft_mtbr").innerHTML = round(reconstructed_fault_tree[basicEventID].mtbr, 5);
        oper_avail_string = round(reconstructed_fault_tree[basicEventID].oper_avail * 100, 5).toString();
        document.getElementById("oper_avail").innerHTML = oper_avail_string.concat(' %');
    }
}