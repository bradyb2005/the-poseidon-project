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
 * @param {string} query - The search term or tag name
 * @param {boolean} isTag - Whether the query is a specific tag filter
 */
async function renderSearchResults(query, isTag = false) {
    const root = document.getElementById('app-root');
    const page = 1; // For pagination, if needed

    root.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Scanning the horizon for ${isTag ? 'tag' : ''} "${query}"...</p>
        </div>
    `;

    try {
        // Construct the URL based on whether we are filtering by tag or keyword
        let url = `http://localhost:8000/search?page=${page}`;
        if (isTag) {
            url += `&tag=${encodeURIComponent(query)}`;
        } else {
            url += `&q=${encodeURIComponent(query)}`;
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch search results');
        const data = await response.json();

        root.innerHTML = `
            <div class="search-results-page">
                <div class="results-header">
                    <h2>Found ${data.total_count || 0} treasures for "${query}"</h2>
                    <button class="back-link" onclick="renderHomepage()">← Back to Home</button>
                </div>

                <div class="res-grid">
                    ${data.items && data.items.length > 0 ? data.items.map(item => `
                        <div class="item-card-mini" onclick="viewRestaurant(${item.restaurant_id})">
                            <span class="price">$${parseFloat(item.price).toFixed(2)}</span>
                            <h3>${item.item_name}</h3>
                            <p class="description">${item.description || 'View restaurant menu for details.'}</p>
                            <div class="item-footer">
                                <div class="tags">
                                    ${item.tags ?item.tags.map(t => `<span class="tag">${t}</span>`).join('') : ''}
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
        root.innerHTML = `
            <div class="error-box">
                <p>The sea is too rough: ${err.message}</p>
                <button class="view-btn" onclick="renderHomepage()">Return to Port</button>
            </div>
        `;
    }
}
