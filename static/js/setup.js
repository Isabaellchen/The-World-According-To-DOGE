var hash = window.location.hash,
	parameters = hash.split("/");
	
var currency = parameters[2];

var xhttp = new XMLHttpRequest();
var service_data;
xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		service_data = JSON.parse(this.responseText);
	}
};
xhttp.open("GET", window.location.protocol + "//" + window.location.host + "/price/" + currency, false);
xhttp.send();
var unit = Number(service_data.value);
var unit_rounded = unit.toFixed(2);
var requested_amount = Number(parameters[1]);
var amount = unit * requested_amount;
var doge_amount = Number(amount).toFixed(8);

var dogecoin_url = 
"dogecoin:" + parameters[0].substring(1) 
+ "?amount=" + doge_amount 
+ "&message=" + service_data.cvalue + currency + "t" + service_data.utc;

function show() {
	new QREnc({ecclevel: 3, input: dogecoin_url, qrdiv: "qrdiv", qrcanv: "qrcanv"});
	new QREnc({ecclevel: 3, input: window.location.href, qrdiv: "qrdiv2", qrcanv: "qrcanv2"});
	document.getElementById("payment_link").href = dogecoin_url;
}
