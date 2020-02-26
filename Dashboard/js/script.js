let app = new Vue({
    el: '#app',
    data: {
        chosenEvent: 'basic_event_1',
        chosenMetric: 'Reliability',
        directory: '/MasterThesis/static/images/',
        png: '.png',
        OriginalFaultTree: null,
        ReconstructedFaultTree: null,
        MinimalCutSets: null
    },
    created() {
        const HTTP = axios.create({
            baseURL: 'https://gaborkevinbarta.com/',
        })
        HTTP.get('MasterThesis/static/data.json')
            .then(response => {
                this.OriginalFaultTree = response.data.OriginalFaultTree;
                this.ReconstructedFaultTree = response.data.ReconstructedFaultTree;
                this.MinimalCutSets = response.data.MinimalCutSets;
            });
    },
    methods: {
        round: function(value, decimals) {
            return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
        },
        formatEventName: function(eventName){
            return eventName.split('_').join(' ');
        },
        getBasicEventNumber: function (basicEventName) {
            return basicEventName.slice(12, basicEventName.length);
        },
        isCheck: function (eventName) {
            return eventName == 'basic_event_1' ? true : false
        },
        metricRadioButton: function (metric) {
            this.chosenMetric = metric;
            let event = this.chosenEvent;
            let source = this.directory.concat(event.concat('_'.concat(metric.concat(this.png))));
            $('#plot').attr('src', source);
        },
        eventRadioButton: function (event) {
            this.chosenEvent = event
            this.fillEventInformation(event)
            let metric = this.chosenMetric;
            let source = this.directory.concat(event.concat('_'.concat(metric.concat(this.png))));
            $('#plot').attr('src', source);
        },
        formatDistribution: function(distribution) {
            if (distribution[0] == 'EXP') {
                let lambda = this.round(distribution[1], 5);
                return 'Exp(&lambda; = '.concat(lambda).concat(')');
            }
            if (distribution[0] == 'WEIBULL') {
                scale = this.round(distribution[1], 5);
                shape = this.round(distribution[2], 5);
                return 'Weibull(&alpha; = '.concat(scale).concat(', &beta; = ').concat(shape).concat(')');
            }
            if (distribution[0] == 'NORMAL') {
                mu = this.round(distribution[1], 5);
                sigma = this.round(distribution[2], 5);
                return 'Normal(&mu; = '.concat(mu).concat(', &sigma; = ').concat(sigma).concat(')');
            }
            if (distribution[0] == 'LOGNORM') {
                mu = this.round(distribution[1], 5);
                sigma = this.round(distribution[2], 5);
                return 'Lognormal(&mu; = '.concat(mu).concat(', &sigma; = ').concat(sigma).concat(')');
            }
            if (distribution[0] == 'UNIDENTIFIED DISTRIBUTION') {
                return 'N/A';
            }
        },
        fillEventInformation: function (event) {
            if (event == 'top_event') {
                document.getElementById("oft_rel_dis").innerHTML = "";
                document.getElementById("rft_rel_dis").innerHTML = "";
                document.getElementById("oft_main_dis").innerHTML = "";
                document.getElementById("rft_main_dis").innerHTML = "";
                document.getElementById("oft_mtbf").innerHTML = "";
                document.getElementById("rft_mtbf").innerHTML = this.round(this.ReconstructedFaultTree[0].mtbf, 5);
                document.getElementById("oft_mtbr").innerHTML = "";
                document.getElementById("rft_mtbr").innerHTML = this.round(this.ReconstructedFaultTree[0].mtbr, 5);
                oper_avail_string = this.round(this.ReconstructedFaultTree[0].oper_avail * 100, 5).toString();
                document.getElementById("oper_avail").innerHTML = oper_avail_string.concat(' %');
            } else {
                basicEventID = parseInt(this.getBasicEventNumber(event), 10);
                document.getElementById("oft_rel_dis").innerHTML = this.formatDistribution(this.OriginalFaultTree[basicEventID].reliability);
                document.getElementById("rft_rel_dis").innerHTML = this.formatDistribution(this.ReconstructedFaultTree[basicEventID].reliability);
                document.getElementById("oft_main_dis").innerHTML = this.formatDistribution(this.OriginalFaultTree[basicEventID].maintainability);
                document.getElementById("rft_main_dis").innerHTML = this.formatDistribution(this.ReconstructedFaultTree[basicEventID].maintainability);
                document.getElementById("oft_mtbf").innerHTML = this.round(this.OriginalFaultTree[basicEventID].mtbf, 5);
                document.getElementById("rft_mtbf").innerHTML = this.round(this.ReconstructedFaultTree[basicEventID].mtbf, 5);
                document.getElementById("oft_mtbr").innerHTML = this.round(this.OriginalFaultTree[basicEventID].mtbr, 5);
                document.getElementById("rft_mtbr").innerHTML = this.round(this.ReconstructedFaultTree[basicEventID].mtbr, 5);
                oper_avail_string = this.round(this.ReconstructedFaultTree[basicEventID].oper_avail * 100, 5).toString();
                document.getElementById("oper_avail").innerHTML = oper_avail_string.concat(' %');
            }
        },
    }
})

