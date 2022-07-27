
$(document).ready(function(){
    $('select').formSelect();
    $('.collapsible').collapsible();
    $('.dropdown-trigger').dropdown();
    $('.sidenav').sidenav();
    $('#sidenav-1').sidenav({ edge: 'left' });
    // Initialize materialize data picker
    $('.datepicker').datepicker({'format': 'yyyy-mm-dd'});
  
    
  });
  