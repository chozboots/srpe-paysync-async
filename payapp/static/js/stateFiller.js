document.getElementById("state").addEventListener("change", function() {
    if (this.value !== "FL") {
        document.getElementById("city").removeAttribute("list");
    } else {
        document.getElementById("city").setAttribute("list", "florida-cities");
    }
});