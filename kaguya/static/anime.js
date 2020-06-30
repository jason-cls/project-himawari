$('.dropdown-menu .status-btn').on('click', function(){
    $('.dropdown-toggle-status').html($(this).html());
})

$('.dropdown-menu .rate-btn').on('click', function(){
    $('.dropdown-toggle-rating').html($(this).html());
})

$(function(){
    $('.table tr[data-href]').each(function(){
        $(this).css('cursor','pointer').hover(
            function(){ 
                $(this).addClass('active'); 
            },  
            function(){ 
                $(this).removeClass('active'); 
            }).click( function(){ 
                document.location = $(this).attr('data-href'); 
            }
        );
    });
});