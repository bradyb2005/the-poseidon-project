// frontend/js/restaurant.js

async function viewRestaurant(restaurantId) {
    const root = document.getElementById('app-root');
    const user = JSON.parse(localStorage.getItem("user")) || {};
    
    // --- DEMO INTERCEPTOR ---
    // Demo working menu
    if (restaurantId === 999 || restaurantId === "999") {
        renderMockMenu(root);
        return; 
    }

    root.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Preparing the menu...</p>
        </div>
    `;
   
    try {
        const [resRes, reviewRes, orderRes] = await Promise.all([
            fetch(`http://localhost:8000/search/details/${restaurantId}`),
            fetch(`http://localhost:8000/reviews/restaurant/${restaurantId}`),
            fetch(`http://localhost:8000/orders`)
        ]);

        if (!resRes.ok) throw new Error('Could not find this restaurant.');

        const restaurant = await resRes.json();
        const reviewData = await reviewRes.json();
        const allOrders = await orderRes.json();

        let validOrder = null;
        if (user.id) {
            validOrder = allOrders.find(o => 
                o.customer_id === user.id && 
                o.restaurant_id === restaurantId && 
                o.status === "completed"
            );
        }

        const isOwner = user.id && restaurant.owner_id === user.id;
        const isUnowned = !restaurant.owner_id;

        window.scrollTo(0, 0);

        root.innerHTML = `
            <div class="restaurant-page">
                <header class="res-hero">
                    <button class="back-link" onclick="renderHomepage()">← Back</button>
                    <div class="owner-controls">
                        ${isOwner ? 
                            `<button class="edit-btn" onclick="openOwnerDashboard(${restaurant.id})">⚙️ Manage Restaurant</button>` : ''}
                        ${isUnowned ? 
                            `<button class="claim-btn" onclick="handleClaim(${restaurant.id})">⚓ Claim Ownership</button>` : ''}
                    </div>
                    <h1>${restaurant.name}</h1>
                    <div class="res-meta">
                        <span>⭐ ${reviewData.average_rating || 'No ratings'}</span>
                        <span>📍 ${restaurant._address}</span>
                        <span>📞 ${restaurant._phone || 'No phone listed'}</span>
                        <span>🕒 ${restaurant._open_time || '??'} - ${restaurant._close_time || '??'}</span>
                        ${isOwner ? `<span class="tag">${restaurant.is_published ? '🟢 Public' : '🔴 Hidden'}</span>` : ''}
                    </div>
                </header>

                <div class="menu-container">
                    <h2>Menu</h2>
                    <div class="menu-grid">
                        ${restaurant.full_menu_details.length > 0 ? 
                            restaurant.full_menu_details.map(item => `
                            <div class="menu-item">
                                <div class="item-header">
                                    <h3>${item.item_name} ${!item.is_available ? '(Out of Stock)' : ''}</h3>
                                    <span class="price">$${parseFloat(item.price).toFixed(2)}</span>
                                </div>
                                <p class="description">${item.description || 'A Poseidon house specialty.'}</p>
                                <div class="item-footer">
                                    <div class="tags">
                                        ${item.tags ? item.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : ''}
                                    </div>

                                    ${isOwner ? 
                                        `<button class="edit-price-btn" onclick="updateItemDetails(${restaurant.id}, '${item.id}', ${item.is_available})">
                                            ${item.is_available ? 'Mark Unavailable' : 'Mark Available'}
                                         </button>` :
                                        `<button class="add-to-cart-btn" ${!item.is_available ? 'disabled' : ''} onclick="addToCart('${item.id}', '${item.item_name}', ${item.price})">
                                            ${item.is_available ? 'Add to Order' : 'Sold Out'}
                                        </button>`
                                    }

                                </div>
                            </div>
                        `).join('') : '<p>This restaurant hasn\'t updated its menu yet.</p>'}
                    </div>
                </div>

                <section class="reviews-section">
                    <h2>Reviews</h2>
                    
                    <div id="review-submission-area">
                        ${validOrder 
                            ? renderReviewForm(restaurantId, validOrder.id) 
                            : `<div class="info-banner">
                                <p>🔒 Only verified customers with a <strong>completed order</strong> can leave a review.</p>
                               </div>`
                        }
                    </div>

                    <div class="reviews-list">
                        ${reviewData.reviews && reviewData.reviews.length > 0 
                            ? reviewData.reviews.map(rev => `
                                <div class="review-card">
                                    <div class="review-header">
                                        <span class="stars">${"⭐".repeat(rev.rating)}</span>
                                        <span class="date">${new Date(rev.created_at).toLocaleDateString()}</span>
                                    </div>
                                    <p class="review-comment">${rev.comment || "No comment left."}</p>
                                    <small class="customer-tag">Customer: ${rev.customer_id}</small>
                                </div>
                            `).join('') 
                            : '<p class="no-reviews">No reviews yet. Be the first to share your experience!</p>'
                        }
                    </div>
                </section>
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
 * --- MOCK MENU RENDERER ---
 * Hardcoded restaurant page for the demo 'Golden Trident'.
 */
function renderMockMenu(root) {
    window.scrollTo(0, 0);
    root.innerHTML = `
        <div class="restaurant-page">
            <header class="res-hero">
                <button class="view-btn" onclick="renderHomepage()">← Back to Home</button>
                <h1>The Golden Trident</h1>
                <div class="res-meta">
                    <span>⭐ 4.9 (Demo)</span>
                    <span>📍 123 Kelowna Way</span>
                    <span>🕒 0:00 - 24:00</span>
                </div>
            </header>

            <div class="menu-container">
                <h2>Menu (Demo Mode)</h2>
                <div class="menu-grid">
                    <div class="menu-item">
                        <div class="item-header">
                            <h3>Kraken Calamari</h3>
                            <span class="price">$14.50</span>
                        </div>
                        <p class="description">Freshly caught and lightly breaded with Poseidon's secret spices.</p>
                        <div class="item-footer">
                            <div class="tags"><span class="tag">Signature</span><span class="tag">Fresh</span></div>
                            <button class="add-to-cart-btn" onclick="addToCart('m1', 'Kraken Calamari', 14.50)">
                                Add to Order
                            </button>
                        </div>
                    </div>

                    <div class="menu-item item-unavailable">
                        <div class="item-header">
                            <h3>Poseidon's Platter (Sold Out)</h3>
                            <span class="price">$22.99</span>
                        </div>
                        <p class="description">A massive feast of the ocean's finest treasures.</p>
                        <div class="item-footer">
                            <div class="tags"><span class="tag">Premium</span></div>
                            <button class="add-to-cart-btn" disabled>Sold Out</button>
                        </div>
                    </div>
                    
                    <div class="menu-item">
                        <div class="item-header">
                            <h3>Seaweed Salad</h3>
                            <span class="price">$8.00</span>
                        </div>
                        <p class="description">Crispy, chilled seaweed with sesame dressing.</p>
                        <div class="item-footer">
                            <div class="tags"><span class="tag">Vegan</span></div>
                            <button class="add-to-cart-btn" onclick="addToCart('m3', 'Seaweed Salad', 8.00)">
                                Add to Order
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * --- HELPER FUNCTION: RENDER REVIEW FORM ---
 */
function renderReviewForm(restaurantId, orderId) {
    return `
        <form class="review-form" onsubmit="submitReview(event, ${restaurantId}, '${orderId}')">
            <h3>Share your experience</h3>
            <p class="order-subtext">Reviewing Verified Order: <strong>#${orderId}</strong></p>
            
            <div class="rating-group">
                <label for="rev-rating">How would you rate your meal?</label>
                <select id="rev-rating" class="rating-select" required>
                    <option value="5">⭐⭐⭐⭐⭐ (Excellent - Perfect in every way!)</option>
                    <option value="4">⭐⭐⭐⭐ (Great - Very tasty, would order again)</option>
                    <option value="3">⭐⭐⭐ (Average - It was okay, but not special)</option>
                    <option value="2">⭐⭐ (Poor - Something went wrong with the order)</option>
                    <option value="1">⭐ (Terrible - Disappointing, would not recommend)</option>
                </select>
            </div>

            <div class="comment-group">
                <label for="rev-comment">Leave a comment (Optional):</label>
                <textarea 
                    id="rev-comment" 
                    placeholder="Tell us what you liked or what we can improve..." 
                    maxlength="1000"
                ></textarea>
                <div class="char-count">Max 1000 characters</div>
            </div>
            
            <button type="submit" class="nav-auth-btn">Submit Review to Poseidon</button>
        </form>
    `;
}

/**
 * --- HELPER: SUBMIT REVIEW ---
 */
async function submitReview(event, restaurantId, orderId) {
    event.preventDefault();

    const userJson = localStorage.getItem("user");

    // Check if user is logged in
    if (!userJson) {
        alert("🔱 Stop! You must be logged in to leave a review.");
        return;
    }
    
    // Grab the values from the form

    const user = JSON.parse(userJson);
    const reviewPayload = {
        restaurant_id: restaurantId,
        order_id: orderId,
        customer_id: user.id,
        rating: parseInt(document.getElementById('rev-rating').value),
        comment: document.getElementById('rev-comment').value.trim() || null
    };

    
    try {
        const response = await fetch('http://localhost:8000/reviews/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reviewPayload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'You can only review orders that have been completed. Please check your order status and try again.');
        }

        alert("🔱 Review accepted! Thank you for your feedback.");
        
        // Refresh the page to show the new review
        viewRestaurant(restaurantId);

    } catch (err) {
        console.error("Submission Error:", err);
        alert(`Batten down the hatches: ${err.message}`);
    }
}

/**
 * --- OWNER: DASHBOARD MODAL ---
 */
async function openOwnerDashboard(restaurantId) {
    const res = await fetch(`http://localhost:8000/search/details/${restaurantId}`);
    const r = await res.json();

    const name = prompt("Edit Name:", r.name) || r.name;
    const address = prompt("Edit Address:", r._address || r.address) || r._address;
    const open = prompt("Open Time (0-2400):", r._open_time) || r._open_time;
    const close = prompt("Close Time (0-2400):", r._close_time) || r._close_time;
    const publish = confirm(`Publish restaurant to the public? Current: ${r.is_published}`);

    const payload = {
        name: name,
        address: address,
        open_time: parseInt(open),
        close_time: parseInt(close),
        is_published: publish
    };

    try {
        const response = await fetch(`http://localhost:8000/restaurants/${restaurantId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            alert("🔱 Logbook updated!");
            viewRestaurant(restaurantId);
        }
    } catch (err) {
        console.error(err);
    }
}

/**
 * --- OWNER: UPDATE ITEM PRICE & AVAILABILITY ---
 */
async function updateItemDetails(restaurantId, itemId) {
    try {
        const res = await fetch(`http://localhost:8000/search/details/${restaurantId}`);
        const restaurant = await res.json();
        
        // Find current item to show existing values in prompts
        const item = restaurant.full_menu_details.find(i => i.id === itemId);

        const newPrice = prompt(`Update price for ${item.item_name}:`, item.price);
        if (newPrice === null) return; // Exit if cancel pressed

        const isAvailable = confirm(`Is ${item.item_name} available today?\n(OK for Available, Cancel for Sold Out)`);

        const updatedMenu = restaurant.full_menu_details.map(i => {
            if (i.id === itemId) return { ...i, price: parseFloat(newPrice), is_available: isAvailable };
            return i;
        });

        const response = await fetch(`http://localhost:8000/restaurants/${restaurantId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_menu_details: updatedMenu })
        });

        if (response.ok) {
            alert("🔱 Menu updated!");
            viewRestaurant(restaurantId);
        }
    } catch (err) {
        alert("Failed to update menu.");
    }
}

/**
 * --- CLAIM OWNERSHIP ---
 */
async function handleClaim(restaurantId) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user || !user.id) {
        alert("🔱 You must be logged in to claim a Restaurant!");
        return;
    }

    if (!confirm("Are you ready to take command of this restaurant?")) return;

    try {
        const response = await fetch(`http://localhost:8000/restaurants/${restaurantId}/owner?owner_id=${user.id}`, {
            method: 'POST'
        });

        if (response.ok) {
            alert("🔱 The crew awaits your orders, Captain!");
            viewRestaurant(restaurantId); // Refresh UI to show the "Edit" button
        } else {
            const err = await response.json();
            alert(`Claim failed: ${err.detail}`);
        }
    } catch (err) {
        console.error("Network Error:", err);
    }
}


/**
 * --- UPDATE ITEM PRICE ---
 * Specifically handles menu pricing updates without affecting restaurant metadata.
 */
async function updateItemPrice(restaurantId, itemId) {
    const newPrice = prompt("Enter new price (e.g. 15.99):");
    if (!newPrice || isNaN(newPrice)) return;

    try {
        // 1. Fetch the latest menu details
        const res = await fetch(`http://localhost:8000/search/details/${restaurantId}`);
        const restaurant = await res.json();

        // 2. Map through current items and update only the targeted ID
        const updatedMenu = restaurant.full_menu_details.map(item => {
            if (item.id === itemId) return { ...item, price: parseFloat(newPrice) };
            return item;
        });

        // 3. Send the entire updated object list to the PUT endpoint
        const response = await fetch(`http://localhost:8000/restaurants/${restaurantId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_menu_details: updatedMenu })
        });

        if (response.ok) {
            alert("🔱 Price updated!");
            viewRestaurant(restaurantId);
        }
    } catch (err) {
        alert("Price update failed.");
    }
}



async function addToCart(itemId, name, price) {
    try {
        
        const customerId = "test_user_1"; 

        const response = await fetch(`http://localhost:8000/cart/${customerId}/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                menu_item_id: itemId,
                quantity: 1
            })
        });

        if (!response.ok) {
            console.error("Backend failed to add item");
        }
    } catch (error) {
        console.error("Network error trying to add to cart:", error);
    }

    alert(`Added ${name} ($${parseFloat(price).toFixed(2)}) to your order!`);
}