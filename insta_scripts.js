function downloadProfilePic() {
    var username = document.getElementById("username").value;
    var resultDiv = document.getElementById("result");

    if (username) {
        resultDiv.innerText = "Downloading...";
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/download?username=" + username, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                resultDiv.innerText = xhr.responseText;
            }
        };
        xhr.send();
    } else {
        resultDiv.innerText = "Please enter a username.";
    }
}