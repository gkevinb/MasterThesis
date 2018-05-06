$(document).ready(function(){
    $("input:radio[name=events]").click(function() {
        var value = $(this).val();
        console.log(value)
        var image_name = value.toLowerCase().replace(/ /g,"_");
        var directory = '/static/images/'
        var png = '.png'
        var source = directory.concat(image_name.concat(png))
        console.log(source)
        $('#plot').attr('src', source);
    });
});
