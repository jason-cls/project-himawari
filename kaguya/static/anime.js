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

// Searchable dropdown
$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".dropdown-menu div").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){
  $("#yearInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".dropdown-menu div").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});