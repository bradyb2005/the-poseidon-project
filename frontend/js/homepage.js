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

        // Calculate current time to show Open/Closed status
        const currentHour = new Date().getHours();

        root.innerHTML = `
            <div class="home-container">
                <section class="hero-banner">
                    <h1>🔱 The Poseidon Project 🔱</h1>
                    <p>High-quality meals, delivered at sea-speed.</p>
                    <div class="search-box">
                        <input type="text" id="main-search" 
                               placeholder="Search for sushi, pizza, or burgers..."
                               onkeydown="if(event.key==='Enter') handleHomeSearch()">
                        <button onclick="handleHomeSearch()">Search</button>
                    </div>
                </section>

                <section class="featured-section">
                    <h2>Trending Now</h2>
                    <div class="horizontal-scroll">
                        ${(data.featured_items || []).map(item => `
                            <div class="item-card-mini">
                                <span class="price">$${item.price}</span>
                                <h4>${item.item_name}</h4>
                                <p class="tag-list">${item.tags ? item.tags.join(', ') : 'Fresh'}</p>
                            </div>
                        `).join('')}
                    </div>
                </section>

                <section class="restaurant-list">
                    <h2>Popular Restaurants</h2>
                    <div class="res-grid">
                        ${data.restaurants.items.map(res => {
                            // Determine if restaurant is currently open
                            const isOpen = currentHour >= res._open_time && currentHour < res._close_time;
                            const statusClass = isOpen ? 'status-open' : 'status-closed';
                            const statusText = isOpen ? 'Open Now' : 'Closed';
                            
                            return `
                                <div class="res-card ${!isOpen ? 'res-closed-fade' : ''}" onclick="viewRestaurant(${res.id})">
                                    <div class="res-badge ${statusClass}">${statusText}</div>
                                    <div class="res-info">
                                        <h3>${res.name}</h3>
                                        <p class="address">📍 ${res._address || 'Local'}</p>
                                        <span class="status-badge">Open until ${res._close_time}:00</span>
                                    </div>
                                    <button class="view-btn">View Menu</button>
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
/**
Search and Navbar logic
 */
function handleHomeSearch() {
    const queryField = document.getElementById('main-search');
    const query = queryField ? queryField.value.trim() : "";
    
    if (query.length >= 2) {
        // If your teammate has built renderSearchResults, call it
        if (typeof renderSearchResults === "function") {
            renderSearchResults(query);
        } else {
            alert(`Searching for "${query}"... (Search results view not yet linked)`);
        }
    } else {
        alert("Please enter at least 2 characters to search.");
    }
}
}

// Add a shadow to the navbar when scrolling
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
    } else {
        nav.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    }
});