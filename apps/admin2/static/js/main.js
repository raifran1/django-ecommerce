$(document).ready(function() {

    var deleteBtn = $('.delete');

    $(deleteBtn).on('click', function(e) {
        e.preventDefault();

        var link = $(this).attr('href');
        var result = confirm('Quer deletar esse veículo?');

        if(result) {
            window.location.href = link;
        }
    });
});