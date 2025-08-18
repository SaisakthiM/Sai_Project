// Async function to fetch timezone info from Abstract API

let currentTime = null; // store the fetched time
let timer = null;       // store interval

async function getTime(region, city) {
    const inputBox = document.querySelector(".result_text");

    try {
        // Show spinner only for initial fetch
        inputBox.classList.add("loading");
        inputBox.value = "Loading...";

        const apiKey = "b4effe8ab1494bcfa6cadfacabd74325"; // replace with your API key
        const location = `${region}/${city}`;
        const url = `https://timezone.abstractapi.com/v1/current_time/?api_key=${apiKey}&location=${location}`;

        let response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        let data = await response.json();
        console.log("API Response:", data);

        // Parse datetime
        currentTime = new Date(data.datetime);

        // Clear any old timer
        if (timer) clearInterval(timer);

        // Function to update input box with date + time
        function updateDisplay() {
            const datePart = currentTime.toLocaleDateString();
            const timePart = currentTime.toLocaleTimeString();
            inputBox.value = `${datePart} ${timePart}`;
        }

        // Update immediately
        updateDisplay();

        // Start ticking every second
        timer = setInterval(() => {
            currentTime.setSeconds(currentTime.getSeconds() + 1);
            updateDisplay();
        }, 1000);

    } catch (error) {
        console.error("Error fetching time:", error);
        inputBox.value = "Invalid region/city or API error!";
    } finally {
        // Hide spinner after fetch
        inputBox.classList.remove("loading");
    }
}


// Button click event
document.querySelector(".button_clock").addEventListener("click", function () {
    let user_city = document.querySelector(".city_input").value.trim();
    let user_region = document.querySelector(".region_input").value.trim();

    getTime(user_region, user_city);
});


