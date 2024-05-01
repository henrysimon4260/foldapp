var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map-container'), {
        zoom: 15,
        center: { lat: 0, lng: 0 } // Default center (can be adjusted)
    });
    // Initialize map and handle geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var marker = new google.maps.Marker({
                position: userLocation,
                map: map
            });
            map.setCenter(userLocation);
            document.getElementById('loading-screen').style.display = 'none';
        }, function() {
            // Handle geolocation error
            handleLocationError(true);
            document.getElementById('loading-screen').style.display = 'none';
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false);
        document.getElementById('loading-screen').style.display = 'none';
    }

    // Initialize autocomplete
    var autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('service-search')
    );

    // Add listener for place changed event
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            return;
        }

        // Clear previous results
        var autocompleteResults = document.getElementById('autocomplete-results');
        autocompleteResults.innerHTML = '';

        // Display best matches in dropdown
        var bestMatches = place.address_components.map(function(component) {
            return component.long_name;
        }).join(', ');
       

        // Show autocomplete dropdown
        autocompleteResults.style.display = 'block';
        // Center map on selected place
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(15);  // Adjust zoom level as needed
        }
        document.getElementById('laundry-options-popup').style.display = 'block';
    });
}

function confirmLaundryOptions() {
    // Retrieve selected options
    var laundryWeight = document.getElementById('laundry-weight').value;
    var detergentType = document.getElementById('detergent-type').value;
    var expressService = document.getElementById('express-service').checked;

    // Handle confirmation logic here
    console.log("Laundry Weight:", laundryWeight);
    console.log("Detergent Type:", detergentType);
    console.log("Express Service:", expressService);

    // Hide laundry options popup
    document.getElementById('laundry-options-popup').style.display = 'none';
    window.location.href = "payment.html";
}

function cancelLaundryOptions() {
    document.getElementById('laundry-options-popup').style.display = 'none';
}

function handleLocationError(browserHasGeolocation, pos) {
    console.log(browserHasGeolocation ?
                'Error: The Geolocation service failed.' :
                'Error: Your browser doesn\'t support geolocation.');
}
