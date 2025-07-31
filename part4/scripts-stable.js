// Stable version - prevent constant refreshing
const API_BASE_URL = 'http://localhost:5000/api/v1';

// Prevent multiple initializations
let isInitialized = false;
let placesLoaded = false;

// Utility functions
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

// Show messages
function showError(message) {
    const existingError = document.querySelector('.error-message');
    if (existingError) existingError.remove();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.insertBefore(errorDiv, document.body.firstChild);
    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccess(message) {
    const existingSuccess = document.querySelector('.success-message');
    if (existingSuccess) existingSuccess.remove();
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    document.body.insertBefore(successDiv, document.body.firstChild);
    setTimeout(() => successDiv.remove(), 3000);
}

// Check authentication - only once
function checkAuthentication() {
    if (isInitialized) return getCookie('token');
    
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
            if (loginLink.tagName === 'A') {
                loginLink.textContent = 'Login';
                loginLink.href = 'login.html';
            } else {
                loginLink.onclick = () => window.location.href = 'login.html';
            }
        } else {
            loginLink.style.display = 'block';
            if (loginLink.tagName === 'A') {
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.onclick = (e) => {
                    e.preventDefault();
                    logout();
                };
            } else {
                loginLink.onclick = logout;
            }
        }
    }
    
    return token;
}

function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

// Display places - prevent re-rendering
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    // Clear only if different content
    const currentPlaces = placesList.children.length;
    if (currentPlaces === places.length && placesLoaded) return;

    placesList.innerHTML = '';
    placesLoaded = true;

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="text-center">No places available.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price_per_night || place.price || 0;
        
        const imageStyle = place.image_url ? 
            `background-image: url('${place.image_url}'); background-size: cover; background-position: center;` :
            `background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 48px; font-weight: 300;`;
        
        placeCard.innerHTML = `
            <div class="place-card-image" style="${imageStyle}">
                ${place.image_url ? '' : '🏠'}
                <button class="favorite-button" onclick="event.stopPropagation(); toggleFavorite('${place.id}')">
                    <svg width="16" height="16" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M16 28c7-4.733 14-10 14-17a6.98 6.98 0 0 0-7-7c-1.8 0-4.058.68-7 2.1C13.058 4.68 10.8 4 9 4a6.98 6.98 0 0 0-7 7c0 7 7 12.267 14 17z"/>
                    </svg>
                </button>
            </div>
            <div class="place-card-content">
                <div class="place-location">${place.city || 'Unknown'}, ${place.country || 'Unknown'}</div>
                <h3>${place.title || 'Untitled Place'}</h3>
                <div class="place-availability">Available dates</div>
                <div class="place-rating">
                    <span class="rating-star">★</span>
                    <span class="rating-value">${place.rating || '4.' + Math.floor(Math.random() * 10)}</span>
                    ${place.reviews_count ? `<span style="color: #717171; margin-left: 4px;">(${place.reviews_count})</span>` : ''}
                </div>
                <div class="place-price">
                    <span class="price-amount">$${place.price_per_night || place.price || 0}</span>
                    <span class="price-period"> night</span>
                </div>
                <div class="price-total">$${Math.round((place.price_per_night || place.price || 0) * 7)} total</div>
            </div>
        `;
        
        // Add click handler without inline onclick
        placeCard.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });
        
        placesList.appendChild(placeCard);
    });
}

// Load places once
async function loadPlaces() {
    if (placesLoaded) return;
    
    try {
        // Try API first
        const response = await fetch(`${API_BASE_URL}/places`);
        if (response.ok) {
            const apiPlaces = await response.json();
            const allPlaces = [...apiPlaces, ...getMockupPlaces()];
            window.allPlaces = allPlaces;
            displayPlaces(allPlaces);
            return;
        }
    } catch (error) {
        console.log('API not available, using mockup data');
    }
    
    // Use mockup data
    const mockupPlaces = getMockupPlaces();
    window.allPlaces = mockupPlaces;
    displayPlaces(mockupPlaces);
}

// Search functionality
function performSearch(query) {
    if (!window.allPlaces) return;
    
    const filteredPlaces = window.allPlaces.filter(place => {
        const searchText = query.toLowerCase();
        return place.title.toLowerCase().includes(searchText) ||
               place.city.toLowerCase().includes(searchText) ||
               place.country.toLowerCase().includes(searchText) ||
               (place.description && place.description.toLowerCase().includes(searchText));
    });
    
    placesLoaded = false; // Allow re-render for search results
    displayPlaces(filteredPlaces);
}

// Price filter
function filterByPrice(maxPrice) {
    if (!window.allPlaces) return;
    
    let filteredPlaces = window.allPlaces;
    
    if (maxPrice !== 'all') {
        filteredPlaces = filteredPlaces.filter(place => {
            const price = place.price_per_night || place.price || 0;
            return price <= parseInt(maxPrice);
        });
    }
    
    placesLoaded = false; // Allow re-render for filter results
    displayPlaces(filteredPlaces);
}

// Favorite toggle
function toggleFavorite(placeId) {
    const button = event.target.closest('.favorite-button');
    if (!button) return;
    
    const svg = button.querySelector('svg');
    if (svg.getAttribute('fill') === 'currentColor') {
        svg.setAttribute('fill', 'none');
        svg.setAttribute('stroke', 'currentColor');
        showSuccess('Removed from favorites');
    } else {
        svg.setAttribute('fill', 'currentColor');
        svg.setAttribute('stroke', 'none');
        showSuccess('Added to favorites');
    }
}

// Authentication functions
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.access_token) {
                setCookie('token', data.access_token);
                showSuccess('Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            } else {
                showError('Login failed: No access token received');
            }
        } else {
            let errorMessage = `Login failed: ${response.status} ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorData.message || errorMessage;
            } catch (e) {
                // Use default error message
            }
            showError(errorMessage);
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

async function registerUser(firstName, lastName, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password
            })
        });

        if (response.ok) {
            showSuccess('Registration successful! You can now log in.');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            let errorMessage = `Registration failed: ${response.status} ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorData.message || errorMessage;
            } catch (e) {
                // Use default error message
            }
            showError(errorMessage);
        }
    } catch (error) {
        console.error('Registration error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

// Initialize only once
document.addEventListener('DOMContentLoaded', () => {
    if (isInitialized) return;
    isInitialized = true;
    
    const currentPage = window.location.pathname.split('/').pop();
    const token = checkAuthentication();
    
    // Page-specific initialization
    if (currentPage === 'index.html' || currentPage === '') {
        // Load places
        loadPlaces();
        
        // Search functionality - add only once
        const searchInputs = document.querySelectorAll('.search-input');
        searchInputs.forEach(input => {
            let searchTimeout;
            input.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    performSearch(e.target.value);
                }, 300);
            });
        });
        
        const heroSearch = document.querySelector('.hero-search input');
        if (heroSearch) {
            let searchTimeout;
            heroSearch.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    performSearch(e.target.value);
                }, 300);
            });
        }
        
        // Price filter
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (e) => {
                filterByPrice(e.target.value);
            });
        }
    }
    
    // Login page
    if (currentPage === 'login.html') {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value.trim();
                const password = document.getElementById('password').value;
                
                if (!email || !password) {
                    showError('Please fill in all fields');
                    return;
                }
                
                await loginUser(email, password);
            });
        }
    }
    
    // Register page
    if (currentPage === 'register.html') {
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const firstName = document.getElementById('first-name').value.trim();
                const lastName = document.getElementById('last-name').value.trim();
                const email = document.getElementById('email').value.trim();
                const password = document.getElementById('password').value;
                
                if (!firstName || !lastName || !email || !password) {
                    showError('Please fill in all fields');
                    return;
                }
                
                await registerUser(firstName, lastName, email, password);
            });
        }
    }
    
    // Place details page
    if (currentPage === 'place.html') {
        initPlaceDetailsPage();
    }
});

// Place details functionality
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

async function loadPlaceDetails(placeId) {
    // First try to find in loaded places
    if (window.allPlaces) {
        const place = window.allPlaces.find(p => p.id === placeId);
        if (place) {
            displayPlaceDetails(place);
            return;
        }
    }
    
    // Try mockup data
    if (typeof getMockupPlace === 'function') {
        const mockupPlace = getMockupPlace(placeId);
        if (mockupPlace) {
            displayPlaceDetails(mockupPlace);
            return;
        }
    }
    
    // Try API
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            return;
        }
    } catch (error) {
        console.log('API not available for place details');
    }
    
    // Show error if place not found
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        placeDetails.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <h2>Place Not Found</h2>
                <p>The place you're looking for doesn't exist.</p>
                <a href="index.html" class="login-button" style="text-decoration: none; margin-top: 20px; display: inline-block;">Back to Places</a>
            </div>
        `;
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    const hostName = place.owner 
        ? `${place.owner.first_name} ${place.owner.last_name}` 
        : 'Host';
    
    const price = place.price_per_night || place.price || 0;
    
    placeDetails.innerHTML = `
        <div style="margin-bottom: 32px;">
            ${place.image_url ? `
                <div style="width: 100%; height: 400px; background-image: url('${place.image_url}'); background-size: cover; background-position: center; border-radius: 12px; margin-bottom: 24px;"></div>
            ` : `
                <div style="width: 100%; height: 400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 72px; margin-bottom: 24px;">🏠</div>
            `}
            
            <h1 style="font-size: 32px; font-weight: 600; color: #222; margin-bottom: 16px;">${place.title || 'Untitled Place'}</h1>
            
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
                <div style="display: flex; align-items: center; gap: 4px;">
                    <span style="color: #FF385C;">★</span>
                    <span style="font-weight: 600;">${place.rating || '4.8'}</span>
                    ${place.reviews_count ? `<span style="color: #717171;">(${place.reviews_count} reviews)</span>` : ''}
                </div>
                <span style="color: #717171;">•</span>
                <span style="color: #717171;">${place.city || 'Unknown'}, ${place.country || 'Unknown'}</span>
            </div>
            
            <div style="border-top: 1px solid #ddd; padding-top: 24px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                    <div>
                        <h3 style="font-size: 22px; font-weight: 600; color: #222; margin-bottom: 8px;">Hosted by ${hostName}</h3>
                        <p style="color: #717171; font-size: 16px;">${place.description || 'A wonderful place to stay.'}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 24px; font-weight: 600; color: #222;">$${price}</div>
                        <div style="color: #717171;">night</div>
                    </div>
                </div>
            </div>
            
            ${place.amenities && place.amenities.length > 0 ? `
                <div style="border-top: 1px solid #ddd; padding-top: 24px; margin-bottom: 24px;">
                    <h3 style="font-size: 22px; font-weight: 600; color: #222; margin-bottom: 16px;">What this place offers</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px;">
                        ${place.amenities.map(amenity => `
                            <div style="display: flex; align-items: center; gap: 12px; padding: 8px 0;">
                                <span>✓</span>
                                <span>${typeof amenity === 'string' ? amenity : amenity.name}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        </div>
    `;

    // Display reviews if they exist
    if (place.reviews && place.reviews.length > 0) {
        const reviewsSection = document.createElement('div');
        reviewsSection.style.borderTop = '1px solid #ddd';
        reviewsSection.style.paddingTop = '24px';
        reviewsSection.innerHTML = `
            <h3 style="font-size: 22px; font-weight: 600; color: #222; margin-bottom: 24px;">
                ${place.reviews.length} review${place.reviews.length !== 1 ? 's' : ''}
            </h3>
        `;
        
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.style.cssText = 'margin-bottom: 24px; padding: 20px; background: #f7f7f7; border-radius: 12px;';
            
            const userName = review.user 
                ? `${review.user.first_name} ${review.user.last_name}` 
                : 'Anonymous';
            const rating = review.rating || 5;
            
            reviewCard.innerHTML = `
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; background: #ddd; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #666; font-weight: 600;">
                        ${userName.charAt(0)}
                    </div>
                    <div>
                        <div style="font-weight: 600; color: #222;">${userName}</div>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <span style="color: #FF385C;">★</span>
                            <span style="font-size: 14px; color: #717171;">${rating}/5</span>
                        </div>
                    </div>
                </div>
                <p style="color: #222; line-height: 1.6;">${review.text || 'No review text provided.'}</p>
            `;
            reviewsSection.appendChild(reviewCard);
        });
        
        placeDetails.appendChild(reviewsSection);
    }
    
    // Show add review section if user is authenticated
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        const token = getCookie('token');
        if (token) {
            addReviewSection.style.display = 'block';
            const addReviewLink = addReviewSection.querySelector('a');
            if (addReviewLink) {
                addReviewLink.href = `add_review.html?id=${place.id}`;
            }
        } else {
            addReviewSection.style.display = 'none';
        }
    }
}

// Initialize place details page
function initPlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = `
                <div style="text-align: center; padding: 40px;">
                    <h2>No Place Selected</h2>
                    <p>Please select a place to view details.</p>
                    <a href="index.html" class="login-button" style="text-decoration: none; margin-top: 20px; display: inline-block;">Browse Places</a>
                </div>
            `;
        }
        return;
    }
    
    loadPlaceDetails(placeId);
}

// Make functions available globally for inline handlers
window.toggleFavorite = toggleFavorite;
window.getPlaceIdFromURL = getPlaceIdFromURL;