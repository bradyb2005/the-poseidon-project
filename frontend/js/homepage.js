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

        let nearbyUrl = 'http://localhost:8000/search/landing';
        // Using a promise-based wrapper for geolocation
        const pos = await new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(resolve, () => resolve(null));
        });

        if (pos) {
            const { latitude, longitude } = pos.coords;
            // If we have location, hit the nearby endpoint instead
            nearbyUrl = `http://localhost:8000/search/nearby?lat=${latitude}&lon=${longitude}`;
        }

        const response = await fetch(nearbyUrl);
        if (!response.ok) throw new Error('Failed to fetch homepage data');
        const data = await response.json();

        const mockItems = [
            {
                price: "12.99",
                item_name: "Poseidon's Platter",
                tags: ["Signature", "Fresh"],
                rating: 4.8,
                reviewCount: 124,
                topReview: "Best seafood I've ever had! The flavors were incredible and the freshness was unmatched."
            },
            {
                price: "18.50",
                item_name: "Trident Tuna Steak",
                tags: ["Premium"],
                rating: null, // No reviews for this one
                reviewCount: 0,
                topReview: null
            },
        ];

        let featuredItems = [];
        if (Array.isArray(data.featured) && data.featured.length > 0) {
            featuredItems = data.featured;
        } else if (data.featured && typeof data.featured === 'object' && data.featured.item_name) {
            featuredItems = [data.featured];
        } else {
            featuredItems = mockItems; // Fallback to mock so it's never undefined
        }

        let restaurantItems = [];
        if (data.restaurants && Array.isArray(data.restaurants.items)) {
            restaurantItems = data.restaurants.items;
        } else if (Array.isArray(data.restaurants)) {
            restaurantItems = data.restaurants;
        } else {
                restaurantItems = [
                    {
                        id: 999,
                        name: "The Golden Trident",
                        _address: "123 Kelowna Way",
                        _open_time: 0,
                        _close_time: 24
                    }
            ];
        }
        
        // Calculate current time to show Open/Closed status
        const currentHour = new Date().getHours();

        root.innerHTML = `
        <div class="home-container">
            <nav class="navbar">
                <span class="nav-brand">🔱 Poseidon</span>
                <div class="nav-links">
                    ${JSON.parse(localStorage.getItem("user")) ? `
                        <span>👤 ${JSON.parse(localStorage.getItem("user")).username}</span>
                        <a href="#" onclick="renderNotifications()">Notifications</a>
                        <a href="#" onclick="handleLogout()">Log out</a>
                    ` : `
                        <a href="#" onclick="renderLogin()">Log In</a>
                        <a href="#" onclick="renderRegister()">Sign Up</a>
                    `}
            </div>
        </nav>
        <section class="hero-banner">
                    <h1>🔱 The Poseidon Project 🔱</h1>
                    <p>High-quality meals, delivered at sea-speed.</p>
                    <form class="search-box" onsubmit="handleSearch(event)">
                        <input 
                            type="text" 
                            id="search-input" 
                            placeholder="Search for food (e.g. Sushi, Burgers)..."
                            required
                        >
                        <button type="submit" class="view-btn">Search</button>
                    </form>
                    <div class="tag-filters">
                        <button class="filter-chip" onclick="handleSearch(null, 'Signature')">⭐ Signature</button>
                        <button class="filter-chip" onclick="handleSearch(null, 'Premium')">🥩 Premium</button>
                        <button class="filter-chip" onclick="handleSearch(null, 'Fresh')">🌿 Fresh</button>
                        <button class="filter-chip" onclick="handleSearch(null, 'Burger')">🍔 Burgers</button>
                    </div>
                </section>

                <section class="featured-section">
                    <h2>Trending Now</h2>
                    <div class="horizontal-scroll">
                        ${featuredItems.map(item => `
                            <div class="item-card-mini">
                                <span class="price">$${item.price}</span>
                                <h4>${item.item_name}</h4>

                                <div class="item-rating">
                                    ${item.rating 
                                        ? `
                                            <span class="stars">⭐ ${item.rating}</span> 
                                            <span class="review-count">(${item.reviewCount})</span>
                                            ${item.topReview ? `<p class="featured-review">"${item.topReview}"</p>` : ''}
                                          ` 
                                        : `<span class="no-reviews">No reviews yet</span>`
                                    }
                                </div>

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
                                    onclick="viewRestaurant(${res.id})"> 
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
async function handleSearch(event, tag = null) {
    if (event) event.preventDefault();

    const inputField = document.getElementById('search-input');
    const query = tag || (inputField ? inputField.value.trim() : "");

    if (query.length >= 2 || tag) {
        if (typeof renderSearchResults === "function") {
            renderSearchResults(query, !!tag);
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

function handleLogout() {
    localStorage.removeItem("user");
    renderHomepage();
}
