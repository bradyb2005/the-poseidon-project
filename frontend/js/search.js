// frontend/js/search.js

/**
 * Search form submission handler
 */
async function handleSearch(event) {
    if (event) event.preventDefault();
    
    const query = document.getElementById('search-input').value;
    if (!query || query.length < 2) return;

    renderSearchResults(query);
}

/**
 * Fetches and displays the search results
 */
async function renderSearchResults(query, page = 1) {
    const root = document.getElementById('app-root');
    

    root.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Scanning the horizon for "${query}"...</p>
        </div>
    `;

    try {
        const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(query)}&page=${page}`);
        const data = await response.json();

        root.innerHTML = `
            <div class="search-results-page">
                <div class="results-header">
                    <h2>Found ${data.total_count} treasures for "${query}"</h2>
                    <button class="back-link" onclick="renderHomepage()">← Back to Home</button>
                </div>

                <div class="results-grid">
                    ${data.items.length > 0 ? data.items.map(item => `
                        <div class="item-card-mini" onclick="viewRestaurant(${item.restaurant_id})">
                            <span class="price">$${parseFloat(item.price).toFixed(2)}</span>
                            <h3>${item.item_name}</h3>
                            <p class="description">${item.description || 'View restaurant menu for details.'}</p>
                            <div class="item-footer">
                                <div class="tags">
                                    ${item.tags.map(t => `<span class="tag">${t}</span>`).join('')}
                                </div>
                                <span class="view-res-text">Order from Restaurant →</span>
                            </div>
                        </div>
                    `).join('') : `
                        <div class="no-results">
                            <p>No treasures found in these waters. Try searching for "Pizza" or "Burger"!</p>
                        </div>
                    `}
                </div>
            </div>
        `;
    } catch (err) {
        root.innerHTML = `<p class="error">The sea is too rough: ${err.message}</p>`;
    }
}