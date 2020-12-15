function setQueryStringParameter(service, service_value, date1, date1_value, date2, date2_value) {
    const params = new URLSearchParams(location.search);
    params.set(service, service_value);
    params.set(date1, date1_value);
    params.set(date2, date2_value);
    window.history.replaceState({}, "", `${location.pathname}?${params}${window.location.hash}`);
} 

function getDatesDpdown(){
    $.ajax({
        type: "GET",
        url: 'https://awsiptracker.evandrobaginski.com/v1',
        crossDomain: true,
        dataType: 'json',
        success: function(response){
            successGetFunction(response);
        } 
    });    
}

// If the jQuery GET call is success, set app.bucket to bucket name retrieved from APGW/Lambda
function successGetFunction(response){
    // app.bucket = text.split("\"")
    // app.bucket = app.bucket[5]
    app.dates_dpdown = response.body;  
    listLength = app.dates_dpdown.length;
    app.most_recent_date = app.dates_dpdown[listLength-1];
    
    let params = new URLSearchParams(document.location.search.substring(1));  
    if(params.has('service') === false && params.has('date1') === false && params.has('date2') === false){
        app.date2 = app.most_recent_date;
    }
}

window.onload = function() {
    getDatesDpdown();
    
    let params = new URLSearchParams(document.location.search.substring(1));
    if(params.has('service') === true && params.has('date1') === true && params.has('date2') === true){
        app.picked = params.get('service');
        app.date1 = params.get('date1');
        app.date2 = params.get('date2');
        app.buttonClickedOnLoad();
    }
}

// If the jQuery call is success, set app.clicked to true so that the table is shown
function successFunction(response){
    app.date1_saved = app.date1,
    app.date2_saved = app.date2,
    app.picked_saved = app.picked.toUpperCase(),
    app.clicked = true,
    app.diffips = response['diff'],
    app.diffips_removed = response['diff_removed'],
    app.diffipsv6 = response['diffv6'],
    app.diffipsv6_removed = response['diffv6_removed'],
    app.ips1 = response['ips1'],
    app.ipsv6_1 = response['ipv6'],
    app.ips2 = response['ips2'],
    app.ipsv6_2 = response['ipv6_2'],
    app.regions = response['regions'],
    app.regions_removed = response['regions_removed'],
    app.regionsv6 = response['regionsv6'],
    app.regionsv6_removed = response['regionsv6_removed']  
}

// If the service selected was ALL, this success function is called instead. 
// This is because the response from the backend API must be handled differently
function successFunctionServiceAll(response){
    app.clicked = true;
    app.response_all = response;
}

