// SHA-256 Functions
function sha256(str) {
    // Transform the string into an arraybuffer
    var buffer = new TextEncoder("utf-8").encode(str);
    return crypto.subtle.digest("SHA-256", buffer).then(function (hash) {
        return hex(hash);
    });
}


function hex(buffer) {
    var hexCodes = [];
    var view = new DataView(buffer);
    for (var i = 0; i < view.byteLength; i += 4) {
        // Using getUint32 reduces the number of iterations needed (we process 4 bytes each time)
        var value = view.getUint32(i);
        // toString(16) will give the hex representation of the number without padding
        var stringValue = value.toString(16);
        // We use concatenation and slice for padding
        var padding = '00000000';
        var paddedValue = (padding + stringValue).slice(-padding.length);
        hexCodes.push(paddedValue);
    }
    return hexCodes.join("");
}

// Add an event listener on the button
document.getElementById("submit").addEventListener("click", button_listener);

// Add an event on the "Enter" button
document.addEventListener("keyup", function (event) {
    if (event.code === "Enter") {
        document.getElementById("submit").click()
    }
});

// Reset all fields when clicking on the logo
document.getElementById("logo").addEventListener("click", reset);

// Check for empty fields
var id_names = ["username", "domain", "password"];
for (var i = 0; i < 3; i++) {
    document.getElementById(id_names[i]).addEventListener("blur", function (test) {
        if (test.target.value.length === 0) {
            test.target.style.border = "2px solid #f00"
        } else {
            test.target.style.border = "2px solid #ccc"
        }
    });

    document.getElementById(id_names[i]).addEventListener("focus", function (test) {
        test.target.style.border = "2px solid #ccc"
    });
}

// Check for the 3 fields and display password if okay
function button_listener() {
    const button = document.getElementById("submit");

    var empty = false
    for (var i = 0; i < 3; i++) {
        if (document.getElementById(id_names[i]).value.length === 0) {
            document.getElementById(id_names[i]).style.border = "2px solid #f00"
            empty = true
        } else {
            document.getElementById(id_names[i]).style.border = "2px solid #ccc"
        }
    }

    if (empty === true) {
        return false
    }

    if (button.className === "password") {
        button.select();
        document.execCommand("copy");
        button.value = "Copied !";
        window.setTimeout(function () {
            convert_input_button()
        }, 1000)
    } else {
        generate_password()
    }
    return true
}


function reset() {
    // Reset all the inputs
    document.getElementById("username").value = "";
    document.getElementById("domain").value = "";
    document.getElementById("password").value = "";

    // Reset the submit button
    if (document.getElementById("submit").className === "password") {
        convert_input_button()
    } else {
        document.getElementById("submit").value = "";
        document.getElementById("submit").className = "";
        document.getElementById("submit").innerText = "Get My Password !";
    }
}


function convert_button_input(password) {
    let a = document.getElementById("submit");
    // Remove the old listener
    a.removeEventListener("click", button_listener);
    // Create the new input
    let b = document.createElement("input");
    b.id = "submit";
    b.setAttribute("readonly", "readonly");
    b.className = "password";
    b.value = password;
    // Create the new listener
    b.addEventListener("click", button_listener);
    // Replace the old button with the new input
    a.parentNode.replaceChild(b, a)
}


function convert_input_button() {
    let a = document.getElementById("submit");
    // Remove the old listener
    a.removeEventListener("click", button_listener);
    // Create the new button
    let b = document.createElement("button");
    b.id = "submit";
    b.innerText = "Get My Password !";
    // Create the new listener
    b.addEventListener("click", button_listener);
    // Replace the old input with the new button
    a.parentNode.replaceChild(b, a);
}


function generate_password() {
    const username = document.getElementById("username").value;
    const domain = document.getElementById("domain").value;
    const password = document.getElementById("password").value;

    // Hash the 3 input and display to the user when done
    sha256(username + domain + password).then(function (digest) {
        let hash = "";
        // Get 1 char every 4 chars
        for (let i = 0; i < 60; i += 4) {
            hash += digest.charAt(i);
        }
        // Convert to Base64 and keep only the first 15 chars
        hash = btoa(hash).substring(0, 15);
        convert_button_input(hash)
    });

}