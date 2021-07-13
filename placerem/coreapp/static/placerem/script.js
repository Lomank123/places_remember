var url = 'api/recollections'

window.onload = function() {
    var rec_id = document.getElementById('id');
    var rec_name = document.getElementById('name');
    var rec_descr = document.getElementById('description');
    var rec_form = document.getElementById('rec_form');


    rec_form.addEventListener('submit', function(evt) {
        evt.preventDefault();
        var vid = rec_id.value;
        var new_url = url + '/';
        var new_method = 'POST';
        var new_data = JSON.stringify({id : vid, name: rec_name.value,
        description: rec_descr.value});

        //new_data["geom"] = ;

        $.ajax({
            method: new_method,
            url: new_url,
            dataType: "json",
            data: new_data,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('Content-Type', 'application/json'); // or will get 500 internal server error
                console.log('new rec beforeSend');
            },
            success: function(){
                console.log('new rec after send');
            }
        })
    })
}
