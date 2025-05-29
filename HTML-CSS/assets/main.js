function greet() {
    alert("First JS function executed!");
    console.log("Button clicked, function executed.");
}

document.getElementById("dropbtn").addEventListener("click", function() {
    alert("Dropdown hovered!");
    console.log("Dropdown hover event triggered.");
});