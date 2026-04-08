// frontend/js/restaurant.js

/**
 * Renders the full menu for a specific restaurant
 * @param {number} restaurantId 
 */
async function viewRestaurant(restaurantId) {
    const root = document.getElementById('app-root');
    
    // loading state
    root.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Preparing the menu...</p>
        </div>
    `;

    try {
        const response = await fetch(`http://localhost:8000/search/details/${restaurantId}`);
        if (!response.ok) throw new Error('Could not find this restaurant.');
        
        const restaurant = await response.json();

        // Scroll to top of the page
        window.scrollTo(0, 0);

        root.innerHTML = `
            <div class="restaurant-page">
                <div class="res-hero">
                    <button class="back-link" onclick="renderHomepage()">← Back to Restaurants</button>
                    <h1>${restaurant.name}</h1>
                    <div class="res-meta">
                        <span>📍 ${restaurant._address || 'Poseidon Bay'}</span>
                        <span>📞 ${restaurant._phone || 'No phone listed'}</span>
                    </div>
                </div>

                <div class="menu-container">
                    <h2>Menu</h2>
                    <div class="menu-grid">
                        ${restaurant.full_menu_details.length > 0 ? 
                            restaurant.full_menu_details.map(item => `
                            <div class="menu-item">
                                <div class="item-header">
                                    <h3>${item.item_name}</h3>
                                    <span class="price">$${parseFloat(item.price).toFixed(2)}</span>
                                </div>
                                <p class="description">${item.description || 'A Poseidon house specialty.'}</p>
                                <div class="item-footer">
                                    <div class="tags">
                                        ${item.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                    </div>
                                    <button class="add-to-cart-btn" onclick="addToCart('${item.id}', '${item.item_name}', ${item.price})">
                                        Add to Order
                                    </button>
                                </div>
                            </div>
                        `).join('') : '<p>This restaurant hasn\'t updated its menu yet.</p>'}
                    </div>
                </div>
            </div>
        `;

    } catch (err) {
        root.innerHTML = `
            <div class="error-box">
                <h2>Batten down the hatches!</h2>
                <p>${err.message}</p>
                <button onclick="renderHomepage()">Return Home</button>
            </div>
        `;
    }
}

/**
Cart placeholder function
 */
function addToCart(itemId, name, price) {
    alert(`Added ${name} ($${price}) to your order!`);
}