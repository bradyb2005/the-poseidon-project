async function renderCartPage() {
    const root = document.getElementById('app-root');
    const user = JSON.parse(localStorage.getItem("user")) || { id: "test_user_1" };
    
    root.innerHTML = `<div class="loading">Loading your treasures...</div>`;

    try {
        const response = await fetch(`http://localhost:8000/cart/${user.id}/items`);
        let cartData = await response.json();

        if (Array.isArray(cartData)) {
            cartData = { items: cartData };
        }

        const items = cartData.items || [];

        root.innerHTML = `
            <div class="cart-page">
                <h1>Your Cart</h1>
                <div class="cart-items">
                    ${items.length > 0 ? 
                        items.map(item => `
                            <div class="cart-item">
                                <span>Item: ${item.menu_item_id || 'Unknown Item'}</span>
                                <span>Qty: ${item.quantity}</span>
                            </div>
                        `).join('') : '<p>Your cart is empty! Time to find some grub.</p>'}
                </div>
                
                ${items.length > 0 ? `
                    <div class="checkout-section">
                        <button class="checkout-btn" onclick="processCheckout()">Place Order</button>
                    </div>
                ` : ''}
                
                <button onclick="renderHomepage()">← Back to Restaurants</button>
            </div>
        `;
    } catch (err) {
        root.innerHTML = `<p>Error loading cart: ${err.message}</p>`;
    }
}