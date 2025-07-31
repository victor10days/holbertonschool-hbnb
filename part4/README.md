# HBnB - Simple Web Client

This is the front-end web client for the HBnB application, built with HTML5, CSS3, and JavaScript ES6.

## Features

- **Responsive Design**: Works on desktop and mobile devices
- **User Authentication**: Login/logout functionality with JWT tokens
- **Places Listing**: View all available places with filtering by price
- **Place Details**: Detailed view of individual places with reviews
- **Review System**: Add and view reviews for places (authenticated users only)

## Files Structure

```
part4/
├── index.html          # Main page with places listing
├── login.html          # User login page
├── place.html          # Individual place details page
├── add_review.html     # Add review form page
├── styles.css          # Main stylesheet
├── scripts.js          # JavaScript functionality
├── images/             # Image assets
│   ├── logo.svg        # Application logo
│   └── icon.png        # Favicon
└── README.md           # This file
```

## Setup Instructions

1. **API Setup**: Make sure the HBnB API (part3) is running on `http://localhost:5000`
2. **CORS Configuration**: The API has been configured with CORS support for client-server communication
3. **File Server**: Serve the files using a local web server:
   - Python: `python -m http.server 8000`
   - Node.js: `npx http-server`
   - Or any other static file server

## Usage

1. **Access the Application**: Open `http://localhost:8000` in your browser
2. **Browse Places**: View available places on the main page
3. **Filter by Price**: Use the price filter dropdown to narrow results
4. **Login**: Click "Login" to authenticate (required for adding reviews)
5. **View Details**: Click "View Details" on any place to see more information
6. **Add Reviews**: When logged in, you can add reviews to places

## API Integration

The client integrates with the following API endpoints:

- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/places` - Fetch all places
- `GET /api/v1/places/{id}` - Fetch specific place details
- `POST /api/v1/places/{id}/reviews` - Add review to a place

## Authentication

- JWT tokens are stored in cookies for session management
- Authenticated users see "Logout" instead of "Login" in the header
- Review functionality is only available to authenticated users
- Unauthenticated users are redirected when trying to access restricted features

## Design Specifications

The design follows these requirements:

- **Cards**: Places and reviews are displayed as cards with consistent styling
- **Margins**: 20px margins for place and review cards
- **Padding**: 10px padding within cards
- **Borders**: 1px solid #ddd borders with 10px border radius
- **Responsive**: Mobile-friendly responsive design
- **Color Scheme**: Modern blue and gray color palette
- **Typography**: Clean Arial font family

## Browser Compatibility

- Modern browsers with ES6 support
- Tested on Chrome, Firefox, Safari, and Edge
- Mobile responsive design

## Development Notes

- All HTML pages are W3C compliant
- JavaScript uses modern ES6+ features (async/await, arrow functions)
- CSS follows modern practices with flexbox and grid layouts
- Error handling and user feedback implemented throughout