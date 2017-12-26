var
	hash = window.location.hash,
	parameters = hash.split("/"),
	currency = parameters[2],
	requested_amount = Number(parameters[1]),
	accordions = document.getElementsByClassName("accordion"),
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
	var
		print_page,
		share_buttons = document.getElementsByClassName('resp-sharing-button__link'),
		comment_text,
		share_url,
		k;

	for (k = 0; k < share_buttons.length; k++) {
		comment_text = "Send%20VALUE%20in%20Dogecoin%20now.".replace(/VALUE/, requested_amount + ' ' + currency);
		share_url = window.location.href.replace(/\#/, '%23');
		share_buttons[k].href = share_buttons[k].href.replace(/INSERT_URL_HERE/g, share_url);
		share_buttons[k].href = share_buttons[k].href.replace(/INSERT_COMMENT_HERE/g, comment_text);
	}

	promise.then(function () {
		var
			that = this,
			unit = Number(service_data.value),
			unit_rounded = unit.toFixed(2),
			amount = unit * requested_amount,
			address = parameters[0].substring(1),
			doge_amount = Number(amount).toFixed(8),
			dogecoin_url =
				"dogecoin:" + address
				+ "?amount=" + doge_amount
				+ "&message=" + service_data.cvalue + currency + "t" + service_data.utc
			,
			i;

		document.getElementById("pay_qr").appendChild(kjua({text: dogecoin_url, render: 'image', size: 200, quiet: 3, fill: '#000'}));
		document.getElementById("share_qr").appendChild(kjua({text: window.location.href, render: 'image', size: 200, quiet: 3, fill: '#000'}));

		document.getElementById("payment_link").href = dogecoin_url;
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

function clipboard() {
	var tempInput = document.createElement("input");
	tempInput.style = "position: absolute; left: -1000px; top: -1000px";
	tempInput.value = window.location.href;
	document.body.appendChild(tempInput);
	tempInput.select();
	document.execCommand("copy");
	document.body.removeChild(tempInput);
	return false;
}

function print_page() {
	accordions[0].classList.toggle('active');
	accordions[0].nextElementSibling.style.display = "block";
	window.print();
	accordions[0].classList.toggle('active');
	accordions[0].nextElementSibling.style.display = "none";

	return false;
}