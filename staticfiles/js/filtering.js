/**
 * @Author: Tushar Agarwal(tusharcoder) <tushar>
 * @Date:   2017-08-06T15:06:28+05:30
 * @Email:  tamyworld@gmail.com
 * @Filename: filtering.js
 * @Last modified by:   tushar
 * @Last modified time: 2017-08-06T16:38:58+05:30
 */



 function triggerCountrySelectEvent(){
   val = $("#country").find(":selected").val();
   var ele = $("#state");
   $.get('/accounts/country/states/?country_id='+val,function(response,status){
     $("#state option").remove();
     var string_ = '<option value="">(All)</option>';
     for (var val in response) {
       val=response[val];
       string_=string_+'<option value="'+val.id+'">'+val.name+'('+val.code+')'+'</option>';
     }
     ele.append(string_)
       });
     //clear the state box
     ele.find("option:selected").removeAttr("selected");
 }

$(document).ready(function() {
if ($("#country").val()!='') {
  val = $("#country").find(":selected").val();
  //trigger select state event for already selected country
  // triggerCountrySelectEvent();
}
$('#country').on('change',function(event) {
  event.preventDefault();
  /* Act on the event */
      triggerCountrySelectEvent();
   });
});

$(document).ready(function() {
  function runSearch(){
    var country = $('#country').find(':selected').val()
    var state = $('#state').find(':selected').val()
    var query = $('#search').val()
    window.location.href = "/?country="+country+"&state="+state+"&query="+query.trim();
  }
  $("#filter_button").on('click',function(event) {
    // event.preventDefault();
    /* Act on the event */
    runSearch();
  });

function runevent(event){
  var ele = $(event.target);
      event.preventDefault();
      runSearch();
}


  $("#country").keydown(function(event) {
    /* Act on the event */
    if (event.which != 13 || event.keyCode != 13)
    return;
    runevent(event);
  });
  $("#state").keydown(function(event) {
    /* Act on the event */
    if (event.which != 13 || event.keyCode != 13)
    return;
    runevent(event);
  });
  $("#search").keydown(function(event) {
    /* Act on the event */
    if (event.which != 13 || event.keyCode != 13)
    return;
    runevent(event);
  });
});
