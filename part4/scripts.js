// API Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1';

// Utility function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Utility function to set cookie
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

// Utility function to delete cookie
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

// Check if user is authenticated
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
        } else {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.onclick = logout;
        }
    }
    
    return token;
}

// Logout function
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

// Get place ID from URL parameters
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.insertBefore(errorDiv, document.body.firstChild);
    setTimeout(() => errorDiv.remove(), 5000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    document.body.insertBefore(successDiv, document.body.firstChild);
    setTimeout(() => successDiv.remove(), 3000);
}

// Login functionality
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
            const errorData = await response.json().catch(() => ({}));
            showError(errorData.error || errorData.message || `Login failed: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

// Show loading state
function showLoading(elementId, message = 'Loading...') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="loading">${message}</div>`;
    }
}

// Fetch places from API
async function fetchPlaces(token) {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        showLoading('places-list', 'Loading places...');
    }
    
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            return places;
        } else {
            console.error('Failed to fetch places:', response.status, response.statusText);
            if (response.status === 404) {
                displayPlaces([]);
            } else {
                showError('Failed to load places. Please try again later.');
                displayPlaces([]);
            }
        }
    } catch (error) {
        console.error('Network error fetching places:', error);
        showError('Network error. Please check your connection and try again.');
        displayPlaces([]);
    }
}

// Display places in the list
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="text-center">No places available.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price_per_night || place.price || 0;
        
        placeCard.innerHTML = `
            <h3>${place.title || 'Untitled Place'}</h3>
            <p><strong>Location:</strong> ${place.city || 'Unknown'}, ${place.country || 'Unknown'}</p>
            <p class="price"><strong>Price per night:</strong> $${place.price_per_night || place.price || 0}</p>
            <p>${place.description || 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        placesList.appendChild(placeCard);
    });
}

// Fetch place details from API
async function fetchPlaceDetails(token, placeId) {
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        showLoading('place-details', 'Loading place details...');
    }
    
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            return place;
        } else {
            console.error('Failed to fetch place details:', response.status, response.statusText);
            if (response.status === 404) {
                if (placeDetails) {
                    placeDetails.innerHTML = '<div class="text-center"><h2>Place Not Found</h2><p>The place you are looking for does not exist.</p></div>';
                }
                showError('Place not found.');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 3000);
            } else {
                if (placeDetails) {
                    placeDetails.innerHTML = '<div class="text-center"><h2>Error</h2><p>Failed to load place details.</p></div>';
                }
                showError('Failed to load place details. Please try again later.');
            }
        }
    } catch (error) {
        console.error('Network error fetching place details:', error);
        if (placeDetails) {
            placeDetails.innerHTML = '<div class="text-center"><h2>Network Error</h2><p>Please check your connection and try again.</p></div>';
        }
        showError('Network error. Please check your connection and try again.');
    }
}

// Display place details
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    const hostName = place.owner 
        ? `${place.owner.first_name} ${place.owner.last_name}` 
        : 'Unknown Host';
    
    const price = place.price_per_night || place.price || 0;
    
    placeDetails.innerHTML = `
        <div class="place-info">
            <h1>${place.title || 'Untitled Place'}</h1>
            <p><strong>Host:</strong> ${hostName}</p>
            <p><strong>Location:</strong> ${place.city || 'Unknown'}, ${place.country || 'Unknown'}</p>
            <p class="price"><strong>Price per night:</strong> $${price}</p>
            <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
            
            <div class="amenities">
                <h3>Amenities</h3>
                <ul>
                    ${place.amenities && place.amenities.length > 0 
                        ? place.amenities.map(amenity => `<li>${amenity.name || amenity}</li>`).join('') 
                        : '<li>No amenities listed</li>'}
                </ul>
            </div>
        </div>
    `;

    // Display reviews if they exist
    if (place.reviews && place.reviews.length > 0) {
        const reviewsSection = document.createElement('div');
        reviewsSection.className = 'reviews-section';
        reviewsSection.innerHTML = '<h3>Reviews</h3>';
        
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            const userName = review.user 
                ? `${review.user.first_name} ${review.user.last_name}` 
                : 'Anonymous';
            const rating = review.rating || 5;
            
            reviewCard.innerHTML = `
                <h4>${userName}</h4>
                <div class="rating">Rating: ${'★'.repeat(rating)}${'☆'.repeat(5 - rating)}</div>
                <p>${review.text || 'No review text provided.'}</p>
            `;
            reviewsSection.appendChild(reviewCard);
        });
        
        placeDetails.appendChild(reviewsSection);
    } else {
        const reviewsSection = document.createElement('div');
        reviewsSection.className = 'reviews-section';
        reviewsSection.innerHTML = '<h3>Reviews</h3><p>No reviews yet. Be the first to leave a review!</p>';
        placeDetails.appendChild(reviewsSection);
    }
}

// Submit review
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                text: reviewText,
                rating: parseInt(rating)
            })
        });

        if (response.ok) {
            showSuccess('Review submitted successfully!');
            // Clear the form
            const reviewForm = document.getElementById('review-form');
            if (reviewForm) {
                reviewForm.reset();
            }
            // Redirect back to place details
            setTimeout(() => {
                const placeId = getPlaceIdFromURL();
                if (placeId) {
                    window.location.href = `place.html?id=${placeId}`;
                }
            }, 1000);
        } else {
            const errorData = await response.json();
            showError(errorData.error || errorData.message || 'Failed to submit review');
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('Network error. Please try again.');
    }
}

// Initialize page based on current page
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop();
    
    // Always check authentication status
    const token = checkAuthentication();
    
    // Page-specific initialization
    switch (currentPage) {
        case 'login.html':
            initLoginPage();
            break;
        case 'index.html':
        case '':
            initIndexPage(token);
            break;
        case 'place.html':
            initPlaceDetailsPage(token);
            break;
        case 'add_review.html':
            initAddReviewPage(token);
            break;
    }
});

// Initialize login page
function initLoginPage() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        const submitButton = loginForm.querySelector('button[type="submit"]');
        
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showError('Please fill in all fields');
                return;
            }
            
            if (!email.includes('@')) {
                showError('Please enter a valid email address');
                return;
            }
            
            if (password.length < 6) {
                showError('Password must be at least 6 characters long');
                return;
            }
            
            // Disable button to prevent double submission
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Logging in...';
            }
            
            try {
                await loginUser(email, password);
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Login';
                }
            }
        });
    }
}

// Initialize index page
function initIndexPage(token) {
    // Fetch and display places
    fetchPlaces(token);
    
    // Initialize price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');
            
            placeCards.forEach(card => {
                const cardPrice = parseInt(card.dataset.price);
                
                if (selectedPrice === 'all' || cardPrice <= parseInt(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// Initialize place details page
function initPlaceDetailsPage(token) {
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        showError('Place not found');
        return;
    }
    
    // Fetch place details
    fetchPlaceDetails(token, placeId);
    
    // Show/hide add review section based on authentication
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
            
            // Set up the add review link
            const addReviewLink = addReviewSection.querySelector('a');
            if (addReviewLink) {
                addReviewLink.href = `add_review.html?id=${placeId}`;
            }
        }
    }
}

// Initialize add review page
function initAddReviewPage(token) {
    // Check authentication - redirect if not logged in
    if (!token) {
        showError('Please log in to add a review');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
        return;
    }
    
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        showError('Place not found');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        return;
    }
    
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const submitButton = reviewForm.querySelector('button[type="submit"]');
        
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review-text').value.trim();
            const rating = document.getElementById('rating').value;
            
            if (!reviewText) {
                showError('Please enter your review');
                return;
            }
            
            if (reviewText.length < 10) {
                showError('Review must be at least 10 characters long');
                return;
            }
            
            if (!rating) {
                showError('Please select a rating');
                return;
            }
            
            // Disable button to prevent double submission
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...';
            }
            
            try {
                await submitReview(token, placeId, reviewText, rating);
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Submit Review';
                }
            }
        });
    }
}