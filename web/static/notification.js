var readingsHeader = "<tr><th>Device</th><th>Time</th><th>Value</th></tr>",
    phonesHeader = "<tr><th>Name</th><th>MAC</th><th>Status</th></tr>";
  
var minuteInSeconds = 60,
    hourInSeconds = 60*minuteInSeconds,
    dayInSeconds = hourInSeconds*24;
    
$(document).ready(function(){
  update();
  setInterval(function(){update()},30000);
});

function formatTime(timestamp){
  
    var date = new Date(parseInt(timestamp*1000));
    return date.toLocaleString();
}

function secondsFrom(timestamp){
  
  var now = new Date().getTime() / 1000 ,
      seconds = now - timestamp;
  
  if (seconds > dayInSeconds) return Math.round(seconds / dayInSeconds) +" days";
  else if (seconds > hourInSeconds) return Math.round(seconds / hourInSeconds) +" hours";
  else if (seconds > minuteInSeconds) return Math.round(seconds / minuteInSeconds) +" minutes";
  else return Math.round(seconds)+ " seconds";
}


var update = function(){
  phones();
  lastReadings();
  
}
var phones = function(){
  
    var $table = $("#phones");
    $table.html(phonesHeader);
    $.ajax({
    url: "home",
    dataType: "json",
    success: function (json) {
        for (var i=0; i< json.results.length;i++){
          var r = json.results[i];
          $table.append("<tr>"+
                          "<td>"+r.name+"</td>"+
                          "<td>"+r.mac+"</td>"+
                          "<td>"+r.status+"</td>"+
                        "</tr>");
        }
      }
    });
    
}
function lastReadings(){
    
    var $table = $("#readings");
    $table.html(readingsHeader);
    $.ajax({
    url: "readings/last",
    dataType: "json",
    success: function (json) {
        for (var i=0; i< json.results.length;i++){
          var r = json.results[i];
          $table.append("<tr>"+
                          "<td>"+r.device+"</td>"+
                          "<td>"+formatTime(r.time)+" ("+secondsFrom(r.time)+" ago)</td>"+
                          "<td>"+r.value+"</td>"+
                        "</tr>");
        }
      }
    });
}