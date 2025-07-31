# HBnB Part 4 - Full-Stack Web Application

This is the complete HBnB (Holberton Airbnb) web application with both frontend and backend integrated.

## Features

### Frontend (Web Client)
- **Airbnb-inspired design** with modern UI/UX
- **User authentication** (login/register)
- **Places listing** with search and filtering
- **Place details** pages with reviews and amenities
- **Review system** for authenticated users
- **Responsive design** for all devices
- **Stable performance** with no flickering or constant refreshing

### Backend (REST API)
- **Flask-based REST API** with Flask-RESTX
- **Swagger documentation** at `/api/v1/`
- **CORS enabled** for cross-origin requests
- **JWT authentication** for secure login
- **Full CRUD operations** for all entities
- **Data persistence** with in-memory storage

## Project Structure

```
part4/
├── hbnb/                    # Backend API
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── persistence/    # Data storage
│   ├── run.py              # Server entry point
│   └── requirements.txt    # Python dependencies
├── index.html              # Main frontend page
├── place.html              # Place details page
├── login.html              # Login page
├── register.html           # Registration page
├── styles.css              # Main stylesheet
├── scripts-stable.js       # Frontend JavaScript
├── mockup-data.js          # Sample data
└── start_backend.py        # Backend startup script
```

## Quick Start

### 1. Start the Backend Server

```bash
# Option 1: Using the startup script (recommended)
python3 start_backend.py

# Option 2: Manual startup
cd hbnb
pip install -r requirements.txt
python3 run.py
```

The backend server will start on `http://localhost:5000`

### 2. Open the Frontend

Simply open `index.html` in your web browser or serve it with a simple HTTP server:

```bash
# Using Python's built-in server
python3 -m http.server 8000

# Then visit http://localhost:8000
```

### 3. Explore the Application

- **Main page**: Browse places, search, and filter
- **Authentication**: Register/login to add reviews
- **Place details**: Click on any place to see details
- **API documentation**: Visit `http://localhost:5000/api/v1/`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Users
- `GET /api/v1/users` - Get all users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user

### Places
- `GET /api/v1/places` - Get all places
- `POST /api/v1/places` - Create place
- `GET /api/v1/places/{id}` - Get place by ID
- `PUT /api/v1/places/{id}` - Update place

### Reviews
- `GET /api/v1/reviews` - Get all reviews
- `POST /api/v1/reviews` - Create review
- `GET /api/v1/reviews/{id}` - Get review by ID
- `PUT /api/v1/reviews/{id}` - Update review
- `DELETE /api/v1/reviews/{id}` - Delete review

### Amenities
- `GET /api/v1/amenities` - Get all amenities
- `POST /api/v1/amenities` - Create amenity
- `GET /api/v1/amenities/{id}` - Get amenity by ID
- `PUT /api/v1/amenities/{id}` - Update amenity

## Frontend Features

### User Interface
- **Airbnb-inspired design** with clean, modern aesthetics
- **Responsive layout** that works on desktop, tablet, and mobile
- **Search functionality** in both header and hero sections
- **Price filtering** with dropdown options
- **Place cards** with images, ratings, and pricing
- **Favorite buttons** for bookmarking places

### Authentication
- **User registration** with form validation
- **User login** with JWT token storage
- **Session persistence** using cookies
- **Protected features** (reviews require login)

### Place Details
- **Comprehensive place information** with images and descriptions
- **Host details** and contact information
- **Amenities listing** with organized display
- **Reviews section** with user ratings and comments
- **Add review functionality** for authenticated users

### Performance
- **Stable rendering** with no flickering or constant refreshing
- **Debounced search** to prevent excessive API calls
- **Efficient DOM manipulation** with minimal re-renders
- **Cached data** to reduce server requests

## Technical Details

### Frontend Stack
- **HTML5** semantic markup
- **CSS3** with Flexbox and Grid layouts
- **JavaScript ES6+** with async/await and arrow functions
- **Fetch API** for HTTP requests
- **JWT handling** for authentication
- **Responsive design** with mobile-first approach

### Backend Stack
- **Flask** web framework
- **Flask-RESTX** for REST API and Swagger docs
- **Flask-CORS** for cross-origin resource sharing
- **PyJWT** for JSON Web Token authentication
- **In-memory storage** with repository pattern

### Data Models
- **User**: first_name, last_name, email
- **Place**: name, location, owner_id, amenities, reviews
- **Review**: content, user_id, place_id, rating
- **Amenity**: name, description

## Development

### Adding New Features
1. **Backend**: Add new endpoints in `app/api/v1/`
2. **Frontend**: Update JavaScript functions in `scripts-stable.js`
3. **UI**: Modify HTML templates and CSS styles

### Testing
- **Backend**: Use Swagger UI at `http://localhost:5000/api/v1/`
- **Frontend**: Open browser developer tools for debugging
- **Integration**: Test full user flows from frontend to backend

### Deployment
- **Backend**: Can be deployed to any Python hosting service
- **Frontend**: Can be served from any static web server
- **Environment**: Update API URLs for production deployment

## Troubleshooting

### Common Issues
1. **Backend won't start**: Check Python dependencies in requirements.txt
2. **CORS errors**: Ensure Flask-CORS is installed and configured
3. **API calls failing**: Verify backend is running on port 5000
4. **Frontend not loading**: Check that all files are in correct locations
5. **Authentication issues**: Clear browser cookies and try again

### Performance Issues
- If pages flicker: Use `scripts-stable.js` instead of `scripts.js`
- If search is slow: Debounce is already implemented
- If images don't load: Check mockup data URLs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Holberton School curriculum.