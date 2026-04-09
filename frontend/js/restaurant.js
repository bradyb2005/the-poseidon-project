// frontend/js/restaurant.js

async function viewRestaurant(restaurantId) {
    const root = document.getElementById('app-root');
    const user = JSON.parse(localStorage.getItem("user")) || {};
    
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

        window.scrollTo(0, 0);

        root.innerHTML = `
            <div class="restaurant-page">
                <header class="res-hero">
                    <button class="back-link" onclick="renderHomepage()">← Back</button>
                    <h1>${restaurant.name}</h1>
                    <div class="res-meta">
                        <span>⭐ ${reviewData.average_rating || 'No ratings'}</span>
                        <span>📍 ${restaurant._address}</span>
                        <span>📞 ${restaurant._phone || 'No phone listed'}</span>
                    </div>
                </header>

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
                                        ${item.tags ? item.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : ''}
                                    </div>
                                    <button class="add-to-cart-btn" onclick="addToCart('${item.id}', '${item.item_name}', ${item.price})">
                                        Add to Order
                                    </button>
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
 * --- HELPER: CART PLACEHOLDER ---
 */
function addToCart(itemId, name, price) {
    alert(`Added ${name} ($${parseFloat(price).toFixed(2)}) to your order!`);
}