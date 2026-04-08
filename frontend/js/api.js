// frontend/js/api.js
// Central API configuration for all frontend pages.
// Update API_BASE if the backend runs on a different host or port.
const API_BASE = "http://localhost:8000";

/**
 * Sends a review to the backend.
 * Triggered by the onsubmit event in the restaurant review form.
 */
async function submitReview(event, restaurantId, orderId) {
    event.preventDefault(); // Prevents the page from refreshing automatically
    
    // Safe extraction of user data
    let user = null;
    try {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            user = JSON.parse(storedUser);
        }
    } catch (parseError) {
        console.error("Critical: User data in localStorage is corrupted.", parseError);
        localStorage.removeItem("user"); // Clear the bad data
    }

    // Check for user and user.id
    if (!user || !user.id) {
        alert("You must be logged in to leave a review!");
        return;
    }

    // Match the exact keys
    const payload = {
        rating: parseInt(ratingValue),
        comment: commentValue,
        order_id: orderId,
        restaurant_id: parseInt(restaurantId),
        customer_id: user.id
    };

    try {
        const response = await fetch(`${API_BASE}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("🔱 Review sent! Poseidon appreciates your feedback.");
            // Refresh the restaurant view to show the new review in the list
            viewRestaurant(restaurantId); 
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || "Could not submit review."}`);
        }
    } catch (error) {
        console.error("API Error:", error);
        alert("The connection to the deep-sea server failed.");
    }
}