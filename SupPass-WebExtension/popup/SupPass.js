/*
#
#    SupPass -- No Credentials Storage. No Problem.
#
#    Copyright (C) 2018 Kevin Delbegue, Johnny201, Yann Loukili, Mathieu Calemard Du Gardin
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
*/

if (typeof browser !== 'undefined') {
    let querying = browser.tabs.query({currentWindow: true, active: true});
    querying.then(onTabs, onError);
} else if (typeof chrome !== 'undefined') {
    chrome.tabs.query({currentWindow: true, active: true}, onTabs);
} else {
    console.log("Unsupported browser");
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


// On submit copy the passwword to the clipboard, on second click display the password
$("form").submit(function (event) {
    let form = this;
    let password_button = $("#password_button");

    event.preventDefault();

    if (password_button.val() == "Get My Password !") {  // On the first click will copy the password to the cliboard
        copy_clipboard(build_password());
        password_button.val("Copied !");
        setTimeout(function () {
            form.submit();
        }, 2000)
    } else if (password_button.val() == "Copied !") {  // On the second click will show the password
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
    input_data_hashed = sha256(username + domain + password);

    // Reset the password and reuse the password variable
    sha256_trunc_password = '';

    // Get 1 character every 4 characters
    for (i = 0; i < 64; i += 4){
        sha256_trunc_password += input_data_hashed.charAt(i);
    }

    base64_password = btoa(sha256_trunc_password);

    final_password = '';
    for (i = 0; i < sha256_trunc_password.length; i += 1){
        if (i % 2 == 0) final_password += base64_password.charAt(i);
        else final_password += sha256_trunc_password.charAt(i);
    }

    // Return the password with the 15 first characters of the password formatted in base64
    return final_password;
}
