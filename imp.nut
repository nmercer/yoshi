
// Alias the GPIO pin as 'button'
 
button <- hardware.pin1;
 
function HttpPostWrapper (url, headers, string) {
    local request = http.post(url, headers, string);
    local response = request.sendsync();
    return response;
}

function HttpGetWrapper (url, headers) {
  local request = http.get(url, headers);
  local response = request.sendsync();
  return response;
}

function buttonPress() {
    local state = button.read();

    if (state == 1) {
        // The button is released
        server.log("Release");
        HttpGetWrapper('http://192.168.1.5:3000/random', '')
    } else {
        // The button is pressed
        server.log("Press");
    }
}
 
// Configure the button to call buttonPress() when the pin's state changes
 
button.configure(DIGITAL_IN_PULLUP, buttonPress);
