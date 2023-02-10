// Onclick of the button
document.querySelector("button").onclick = function () {
// Call python's random_python function
eel.pg_home()(function(number){
	// Update the div with a random number returned by python
	document.querySelector(".pg_home").innerHTML = number;
})
}