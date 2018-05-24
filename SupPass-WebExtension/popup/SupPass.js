if (typeof browser !== 'undefined') {
    let querying = browser.tabs.query({currentWindow: true, active: true});
    querying.then(onTabs, onError);
} else if (typeof chrome !== 'undefined') {
    chrome.tabs.query({currentWindow: true, active: true}, onTabs);
} else {
    console.log("Unsupported navigator");
}


// Fetch current domain
function onTabs(tabs) {
// tab.url requires the tabs`permission
    for (let tab of tabs) {
        let httpDomainFilter = /^https?:\/\/[^\.]*?\.?([^\/\.]+\.[\w]+)\//;
        let match = httpDomainFilter.exec(tab.url);
        if (match) {
            $("#domain").val(match[1]);
        }
    }
}


function onError(error) {
    console.log(`Error: ${error}`);
}


// On submit display the password, on second click copy to clipboard
$("form").submit(function (event) {
    let form = this;
    let password_button = $("#password_button");

    event.preventDefault();

    if (password_button.val() !== "Get My Password !") {
        copy_clipboard(password_button.val());
        password_button.val("Copied !");
        setTimeout(function () {
            form.submit();
        }, 2000)
    } else {
        password_button.val(build_password());
    }
});


function copy_clipboard(password) {
    let hidden_input = document.createElement("input");
    hidden_input.setAttribute("value", password);
    document.body.appendChild(hidden_input);
    hidden_input.select();
    document.execCommand("copy");
    document.body.removeChild(hidden_input);
}


function build_password() {
    // Get the username, domain and password from the form
    let username = $("#username").val();
    let domain = $("#domain").val();
    let password = $("#password").val();

    // Concatenate the 3 variables, get the SHA-256 of the result
    let hash = sha256(username + domain + password);

    // Reset the password and reuse the password variable
    password = "";

    // Get 1 character every 4 characters
    for (let i = 0; i < 60; i += 4) {
        password += hash.charAt(i);
    }

    // Return the password with the 15 first characters of the password formatted in base64
    return btoa(password).substring(0, 15);
}