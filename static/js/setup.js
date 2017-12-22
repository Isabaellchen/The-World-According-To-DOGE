var
	hash = window.location.hash,
	parameters = hash.split("/"),
	currency = parameters[2],
	promise,
	service_data;

promise = new Promise(function (resolve, reject) {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", window.location.protocol + "//" + window.location.host + "/price/" + currency, true);
	xhttp.onload = function () {
		if (this.status >= 200 && this.status < 300) {
			service_data = JSON.parse(this.responseText);
			resolve();
		}
	};
	xhttp.send();
});



function show() {
	promise.then(function () {
		var
			that = this,
			unit = Number(service_data.value),
			unit_rounded = unit.toFixed(2),
			requested_amount = Number(parameters[1]),
			amount = unit * requested_amount,
			address = parameters[0].substring(1),
			doge_amount = Number(amount).toFixed(8),
			dogecoin_url =
				"dogecoin:" + address
				+ "?amount=" + doge_amount
				+ "&message=" + service_data.cvalue + currency + "t" + service_data.utc
			,
			accordions = document.getElementsByClassName("accordion"),
			i;

		document.getElementById("pay_qr").appendChild(kjua({text: dogecoin_url, render: 'image', size: 200, quiet: 3, fill: '#000'}));
		document.getElementById("share_qr").appendChild(kjua({text: window.location.href, render: 'image', size: 200, quiet: 3, fill: '#000'}));

		document.getElementById("payment_link").href = dogecoin_url;
		document.getElementById("share_link").href = window.location.href;
		document.getElementById("amount").innerHTML = requested_amount;
		document.getElementById("request_currency").innerHTML = currency;
		document.getElementById("currency_currency").innerHTML = currency;
		document.getElementById("address").innerHTML = address;
		document.getElementById("rate").innerHTML = service_data.cvalue;
		document.getElementById("timestamp").innerHTML = new Date(service_data.utc * 1000).toISOString();
		document.getElementById("finaldoge").innerHTML = doge_amount;

		for (i = 0; i < accordions.length; i++) {
			accordions[i].addEventListener("click", function () {
				if (that.activeAccordion) {
					that.activeAccordion.classList.toggle("active");
					that.activeAccordion.nextElementSibling.style.display = "none";
				}
				/* Toggle between adding and removing the "active" class,
				to highlight the button that controls the panel */
				this.classList.toggle("active");

				/* Toggle between hiding and showing the active panel */
				var panel = this.nextElementSibling;
				if (panel.style.display === "block") {
					panel.style.display = "none";
				} else {
					panel.style.display = "block";
				}
				that.activeAccordion = this;
			});
		}
		if (accordions.length) {
			accordions[0].click();
		}
	});
}