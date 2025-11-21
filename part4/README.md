# HBnB Frontend Application

A modern web application frontend for the HBnB (Holberton BnB) platform, providing a user-friendly interface for browsing and reviewing rental properties.

## Project Structure

```
part4/
├── index.html          # Main page - displays list of places
├── login.html          # User authentication page
├── place.html          # Individual place details page
├── add_review.html     # Review submission page
├── scripts.js          # JavaScript functionality
├── styles.css          # Application styling
└── images/             # Image assets
    ├── logo.png
    └── icon.png
```

## Features

### User Authentication
- Secure login system with JWT token authentication
- Cookie-based session management
- Automatic authentication state handling

### Place Browsing
- Display all available rental properties
- Dynamic price filtering (Under $50, $100, $200)
- Grid-based responsive layout
- Quick access to detailed place information

### Place Details
- Comprehensive property information
- Host details
- Amenities list
- User reviews with star ratings
- Conditional "Add Review" button for authenticated users

### Review System
- Submit reviews for places
- Rate places from 1-5 stars
- Protected access (login required)
- Automatic redirection after submission

## Setup Instructions

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Running HBnB API backend (default: `http://localhost:5000`)

### Configuration

1. Update the API endpoint in `scripts.js` if needed:
```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1';
```

2. Ensure your backend API has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### Running the Application

1. Simply open `index.html` in your web browser, or
2. Use a local development server:
```bash
python -m http.server 8000
# Then navigate to http://localhost:8000
```

## Usage

### Browsing Places
1. Open `index.html` in your browser
2. View all available places
3. Use the price filter dropdown to refine results
4. Click "View Details" to see more information

### Logging In
1. Click "Login" in the navigation
2. Enter your credentials
3. Upon successful login, you'll be redirected to the main page
4. The login link will be hidden when authenticated

### Viewing Place Details
1. Click "View Details" on any place card
2. View comprehensive information including:
   - Place name and description
   - Host information
   - Price per night
   - Available amenities
   - User reviews

### Adding Reviews
1. Must be logged in
2. Navigate to a place details page
3. Click "Add Review" button
4. Fill in your review text
5. Select a rating (1-5 stars)
6. Submit the form
7. Automatically redirected back to place details

## API Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | POST | User authentication |
| `/places` | GET | Fetch all places |
| `/places/{id}` | GET | Fetch specific place details |
| `/reviews` | POST | Submit a new review |

## Technologies Used

- **HTML5** - Structure and semantics
- **CSS3** - Styling and responsive design
- **JavaScript (ES6+)** - Dynamic functionality
- **Fetch API** - HTTP requests
- **JWT** - Token-based authentication

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Design Features

### Responsive Layout
- Mobile-first design approach
- Grid-based place cards
- Flexible containers

### User Experience
- Intuitive navigation
- Clear visual hierarchy
- Consistent styling across pages
- Loading states and error handling

### Security
- Token-based authentication
- HTTP-only cookies
- Protected routes for authenticated users

## Development Notes

### Cookie Management
The application uses cookies to store JWT tokens:
- Token name: `token`
- Default expiration: 7 days
- Path: `/` (site-wide)

### Authentication Flow
1. User submits credentials
2. API returns JWT token
3. Token stored in cookie
4. Token included in subsequent API requests
5. Authentication state checked on page load

### Error Handling
- Login failures display alert messages
- API errors logged to console
- User-friendly error messages
- Graceful fallbacks for missing data

## Maintenance

### Updating Styles
- Edit `styles.css` for visual changes
- Follows mobile-first responsive design
- Uses CSS Grid and Flexbox

### Adding Features
- Extend `scripts.js` with new functions
- Follow existing code structure
- Maintain consistent error handling

### Testing Checklist
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Browse all places
- [ ] Test price filtering
- [ ] View place details
- [ ] Submit review (authenticated)
- [ ] Access protected pages (unauthenticated)
- [ ] Test on multiple browsers

## License

Copyright © 2024 HBnB. All rights reserved.
