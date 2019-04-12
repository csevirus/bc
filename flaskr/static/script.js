var url = ""
function fun(vars) {
    url = vars;
}
var user = {
  lang: "",
  code: "",
  timetaken: 300,
};
function langSelect() {
  user.lang = document.getElementById("language").value;
  document.getElementById("code").disabled = false;
}
// returns char for corresponding keycode
function getChar(event) {
  if (event.keyCode == 13)
    return "\n";
  if (event.which == null) {
    // Return the char if not a special character
    return String.fromCharCode(event.keyCode); // IE
  } else if (event.which != 0 && event.charCode != 0) {
    return String.fromCharCode(event.which); // Other Browsers
  } else {
    return null; // Special Key Clicked
  }
}
var countdown = {
  minutes: 5,
  seconds: 0,
  x: 0,
  charcount: 0,
  myClock: function() {
    if (countdown.seconds == 0) {
      countdown.minutes = countdown.minutes - 1;
      countdown.seconds = 59;
    } else {
      countdown.seconds = countdown.seconds - 1;
    }
    if (countdown.seconds > 9)
    document.getElementById("timer").innerHTML = "<strong>TimeLeft </strong> : 0" + countdown.minutes + ":" + countdown.seconds;
    else {
      document.getElementById("timer").innerHTML = "<strong>TimeLeft </strong> : 0" + countdown.minutes + ":0" + countdown.seconds;
    }
    if (countdown.minutes < 0) {
      countdown.stop();
    }
  },
  clock: function() {
    x = setInterval(countdown.myClock, 1000);
  },
  stop: function() {
    user.timetaken = 300 - (countdown.minutes)*60 + countdown.seconds ;
    document.getElementById("timer").innerHTML = "<strong>TimeLeft </strong> : EXPIRED";
    clearInterval(x);
    countdown.submit();
  },
  charpress: function(event) {
    countdown.charcount += 1;
    document.getElementById("charcount").innerHTML = " <strong>CharacterCount :</strong>" + countdown.charcount;
    var char = getChar(event);
    if (char != null)
      user.code += char;
    event.preventDefault();
    document.getElementById("code").value += "*";
  },
  retry: function() {
    document.getElementById("code").blur();
    user.code = "";
    countdown.charcount = 0;
    document.getElementById("charcount").innerHTML = " <strong>CharacterCount :</strong> " + countdown.charcount;
    document.getElementById("code").value = "";
  },
  submit: function() {
    // display code written so far and the result
    document.getElementById("SubmitButton").disabled = true;
    var request = new XMLHttpRequest();
    request.open('POST',url,true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
      if (request.readyState === 4 && request.status === 200) {
          var result = JSON.parse(request.responseText);
          window.location.replace('/solver/submission/'+request.responseText)
      }
    };
    request.send(JSON.stringify(user));
  }
}
function preventBackspace(event){
  if (event.keyCode == 8 || event.charCode == 8) {
    event.preventDefault();
    document.getElementById("code").blur();
    alert("Backspace is not allowed here");
    return;
  }
}
function noPaste(event) {
  event.preventDefault();
  countdown.retry();
  alert("You cannot paste here ... it's cheating");
}
