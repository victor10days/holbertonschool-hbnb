const API_BASE_URL = 'http://localhost:5000/api/v1';

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function handleLogin() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

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
                    setCookie('token', data.access_token, 7);
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login. Please try again.');
            }
        });
    }
}

function checkAuthentication() {
    const token = getCookie('token');

    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (token) {
            loginLink.style.display = 'none';
        } else {
            loginLink.style.display = 'block';
        }
    }

    return token;
}

async function fetchPlaces() {
    const token = checkAuthentication();

    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price);

        card.innerHTML = `
            <h3>${place.name}</h3>
            <p class="price">$${place.price} per night</p>
            <button class="details-button" onclick="window.location.href='place.html?place_id=${place.id}'">View Details</button>
        `;

        placesList.appendChild(card);
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');

            placeCards.forEach(card => {
                const price = parseFloat(card.getAttribute('data-price'));

                if (selectedPrice === 'all') {
                    card.style.display = 'block';
                } else {
                    const maxPrice = parseFloat(selectedPrice);
                    card.style.display = price <= maxPrice ? 'block' : 'none';
                }
            });
        });
    }
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

async function fetchPlaceDetails(placeId) {
    const token = checkAuthentication();

    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');

    if (!placeDetails) return;

    placeDetails.innerHTML = '';

    const hostName = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown';

    placeDetails.innerHTML = `
        <h1>${place.name}</h1>
        <div class="place-info">
            <p><strong>Host:</strong> ${hostName}</p>
            <p><strong>Price:</strong> $${place.price} per night</p>
            <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
        </div>
        <div class="amenities">
            <h3>Amenities</h3>
            <ul>
                ${place.amenities && place.amenities.length > 0
                    ? place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')
                    : '<li>No amenities listed</li>'}
            </ul>
        </div>
    `;

    if (place.reviews) {
        displayReviews(place.reviews);
    }

    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block';
        } else {
            addReviewSection.style.display = 'none';
        }
    }
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');

    if (!reviewsList) return;

    reviewsList.innerHTML = '';

    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';

        const reviewerName = review.user ? `${review.user.first_name} ${review.user.last_name}` : 'Anonymous';
        const stars = '⭐'.repeat(review.rating || 0);

        card.innerHTML = `
            <p class="reviewer-name">${reviewerName}</p>
            <p class="rating">Rating: ${stars}</p>
            <p>${review.text || review.comment || 'No comment provided'}</p>
        `;

        reviewsList.appendChild(card);
    });
}

function handleAddReview() {
    const token = checkAuthentication();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;

            try {
                const response = await fetch(`${API_BASE_URL}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating),
                        place_id: placeId,
                        user_id: 'placeholder'
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                    setTimeout(() => {
                        window.location.href = `place.html?place_id=${placeId}`;
                    }, 1000);
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('An error occurred while submitting the review. Please try again.');
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const page = path.substring(path.lastIndexOf('/') + 1);

    if (page === 'login.html' || page === '') {
        handleLogin();
    } else if (page === 'index.html') {
        checkAuthentication();
        fetchPlaces();
        setupPriceFilter();
    } else if (page === 'place.html') {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(placeId);
        }
    } else if (page === 'add_review.html') {
        handleAddReview();
    }
});
