// Date validation
function checkValidation() {
    let today = new Date();
    today.setHours(0,0,0,0); // allow today
    let startDateField = document.getElementById('stockStartDate').value;
    let endDateField = document.getElementById('stockEndDate').value;

    let startDate = new Date(document.getElementById('stockStartDate').value);
    let endDate = new Date(document.getElementById('stockEndDate').value);
    let data = document.getElementById('transactionData');

    let upload = document.getElementById('ownFile');
    let fileField = document.getElementById('file');

    var conditionStatus = true;


    /*------------------            Check Date           --------------------*/

    // Condition 1: start DATE > end Date
    if (startDate > endDate) {
        alert('Invalid Date !!! (StartDate should be smaller than endDate)');
        conditionStatus = false;
        return false;
    }

     // Condition 2: end Date > System Date 
    if (endDate > today) {
        alert('Invalid endDate !!! ');
        conditionStatus = false;
        return false;
    }

    /*------------------            Check emptyfield           --------------------*/

    if ((data.checked == true) && (upload.checked == true) && (fileField.files.length == 0)) {
        alert('You have not upload the file !!!');
        conditionStatus = false;
        return false;
    }

    if ((data.checked == true) && (!startDateField || !endDateField )) {
        alert('You have not enter the date !!!');
        conditionStatus = false;
        return false;
    }

    if (conditionStatus) {
        actionStatus();
    }
    

}


// Dynamic Control on Display
function option() {
    let data = document.getElementById('transactionData');
    let options = document.getElementsByClassName('second');
    let upload = document.getElementById('ownFile');
    let stockCategory = document.getElementById('stockCategory');
    let download = document.getElementById('download');

    // Display Transaction section if is selected
    if (data.checked == true) {
        for (var i = 0; i < options.length; i++) {
            options[i].style.display = 'block';
        }

        // Hide stockCategory if upload
        if (upload.checked == true) {
            stockCategory.style.display = 'none';

        }

        // Show stockCategory
        else if (download.checked == true) {
            stockCategory.style.display = 'block';

        }
    }

    // Hide Transaction section if not selected
    else {
        for (var i = 0; i < options.length; i++) {
            options[i].style.display = 'none';
        }

        stockCategory.style.display = 'block';
    }

    // Hide 
}


function actionStatus() {
    let status = document.getElementById('status');
    let data = document.getElementById('transactionData');
    let code = document.getElementById('code');

    let stockCat = document.getElementById('stockCatResult').value;

    // Remind
    if ((data.checked == true) || (code.checked == true && stockCat == 'All')) {
        status.innerHTML = 'It takes a longer time to access data in certain category, please wait !';
        status.style.color = 'red';
        status.style.fontSize = '120%';
    }
}


// Welcome Statement
function ask() {
    let username = prompt('Please enter your name: ');
    let heading = document.getElementById('heading');
    heading.innerHTML = username + ', welcome to the NASDAQ Stock Exchange Scraper';
}