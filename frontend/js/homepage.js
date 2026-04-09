// frontend/js/homepage.js

async function renderHomepage() {
    const root = document.getElementById('app-root');

    // Loading state
    root.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Gathering fresh ingredients...</p>
        </div>
    `;

    try {

        const response = await fetch('http://localhost:8000/search/landing');
        if (!response.ok) throw new Error('Failed to fetch homepage data');
        const data = await response.json();

        const featuredItems = Array.isArray(data.featured) 
            ? data.featured 
            : (data.featured ? [data.featured] : []);

        const restaurantItems = (data.restaurants && Array.isArray(data.restaurants.items)) 
            ? data.restaurants.items 
            : [];

        // Calculate current time to show Open/Closed status
        const currentHour = new Date().getHours();

        root.innerHTML = `
            <div class="home-container">
                <section class="hero-banner">
                    <h1>🔱 The Poseidon Project 🔱</h1>
                    <p>High-quality meals, delivered at sea-speed.</p>
                    <form class="search-box" onsubmit="handleSearch(event)">
                        <input 
                            type="text" 
                            id="search-input" 
                            placeholder="Search for food (e.g. Sushi, Pizza)..."
                            required
                        >
                        <button type="submit" class="view-btn">Search</button>
                    </form>
                </section>

                <section class="featured-section">
                    <h2>Trending Now</h2>
                    <div class="horizontal-scroll">
                        ${featuredItems.map(item => `
                            <div class="item-card-mini">
                                <span class="price">$${item.price}</span>
                                <h4>${item.item_name}</h4>
                                <p class="tag-list">
                                    ${Array.isArray(item.tags) ? item.tags.join(', ') : (item.tags || 'Fresh')}
                                </p>
                            </div>
                        `).join('')}
                    </div>
                </section>

                <section class="restaurant-list">
                    <h2>Popular Restaurants</h2>
                    <div class="res-grid">
                        ${restaurantItems.map(res => {
                            // Determine if restaurant is currently open
                            const isOpen = currentHour >= res._open_time && currentHour < res._close_time;
                            const statusClass = isOpen ? 'status-open' : 'status-closed';
                            const statusText = isOpen ? 'Open Now' : 'Closed';
                            
                            return `
                                <div class="res-card ${!isOpen ? 'res-closed-fade' : ''}"
                                    onclick="viewRestaurant(${res.id})"> <div class="res-badge ${statusClass}">${statusText}</div>
                                    <div class="res-badge ${statusClass}">${statusText}</div>
                                    <div class="res-info">
                                        <h3>${res.name}</h3>
                                        <p class="address">📍 ${res._address || 'Local'}</p>
                                        <span class="status-detail">Hours: ${res._open_time}:00 - ${res._close_time}:00</span>
                                    </div>
                                    <button class="view-btn">
                                        ${isOpen ? 'View Menu' : 'See Menu'}
                                    </button>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </section>
            </div>
        `;
        window.scrollTo(0, 0);
    } catch (err) {
        console.error("Homepage Error:", err);
        root.innerHTML = `
            <div class="error-box">
                <h3>Oops! Something went wrong.</h3>
                <p>${err.message}</p>
                <button onclick="renderHomepage()">Try Again</button>
            </div>
        `;

    }
}
/**
Search and Navbar logic
 */
async function handleSearch(event) {
    if (event) event.preventDefault(); 
    
    const queryField = document.getElementById('search-input');
    const query = queryField ? queryField.value.trim() : "";
    
    if (query.length >= 2) {
        // This calls the function inside search.js file
        if (typeof renderSearchResults === "function") {
            renderSearchResults(query);
        } else {
            console.error("search.js is not loaded yet!");
        }
    } else {
        alert("Please enter at least 2 characters to search.");
    }
}

// Add a shadow to the navbar when scrolling
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.navbar');
    if (nav) {
        if (window.scrollY > 50) {
            nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
        } else {
            nav.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
        }
    }
});