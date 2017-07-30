$(document).ready(function() {
if ($("#country").val()!='') {
  val = $("#country").find(":selected").val();
  $("#state option").each(function(){
    if ($(this).data('country')==val) {
      $(this).show();
    }else{
      $(this).hide();
    }
  });
}
$('#country').on('change',function(event) {
  event.preventDefault();
  /* Act on the event */
  val = $("#country").find(":selected").val();
  $("#state option").each(function(){
    if ($(this).data('country')==val) {
      $(this).show();
    }else{
      $(this).hide();
    }
  });
});
});

$(document).ready(function() {
  function runSearch(){
    var country = $('#country').find(':selected').val()
    var state = $('#state').find(':selected').val()
    var query = $('#search').val()
    // if(query.trim()!=''||query!=undefined)
    // {
    window.location.href = "/?country="+country+"&state="+state+"&query="+query.trim();
    // }else{
    //   window.location.href = "/?country="+country+"&state="+state;
    // }
  }
  $("#filter_button").on('click',function(event) {
    // event.preventDefault();
    /* Act on the event */
    runSearch();
  });

function runevent(){
  var ele = $(event.target);
  // if ((function(val){return ['country','state','search'].indexOf(val)})(ele.attr("id"))){
    // if (event.which == 13 || event.keyCode == 13) {
      event.preventDefault();
      runSearch();
    // }
  // }
}
  $("#country").keydown(function(event) {
    /* Act on the event */
    if (event.which != 13 || event.keyCode != 13)
    return;
    runevent();
  });
  $("#state").keydown(function(event) {
    /* Act on the event */
    if (event.which != 13 || event.keyCode != 13)
    return;
    runevent();
  });
  $("#search").keydown(function(event) {
    /* Act on the event */
    if (event.which != 13 || event.keyCode != 13)
    return;
    runevent();
  });
});