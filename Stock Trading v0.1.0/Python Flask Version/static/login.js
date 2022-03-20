function checkLogin() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if (username.length + password.length <=0 ){
        if (username.length <= 0) {
            alert("Username must be input !")
            return false;
        }
        else if (password.length <= 0) {
            alert("Password must be input !")
            return false;
        }
    }
}
