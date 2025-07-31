# HBnB Client Setup & Testing Guide

## Quick Start

### 1. Start the API Server

```bash
# Navigate to the API directory
cd ../part3/hbnb

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the API server
python run.py
```

The API should be running on `http://localhost:5000`

### 2. Start the Client Server

```bash
# Navigate to the client directory
cd part4

# Start the simple Python server
python server.py

# Or use Python's built-in server
python -m http.server 8000

# Or use Node.js http-server
npx http-server
```

The client should be accessible at `http://localhost:8000`

### 3. Test the Connection

Visit `http://localhost:8000/test.html` to test API connectivity and basic functionality.

## Complete Testing Workflow

### Step 1: Test API Connection
1. Open `http://localhost:8000/test.html`
2. Click "Test API Connection"
3. Should see "✅ API Connection Successful!"

### Step 2: Test Main Application
1. Open `http://localhost:8000/index.html`
2. Should see places loading (or empty state if no places exist)
3. Test price filtering

### Step 3: Test Authentication
1. Go to login page: `http://localhost:8000/login.html`
2. Try logging in with test credentials:
   - Email: `admin@hbnb.com` (if exists)
   - Password: `admin123` (if exists)

### Step 4: Create Test Data (Optional)

If no places exist, you can create test data via API:

```bash
# Create a test user (if registration is available)
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login to get token
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Create a test place (replace TOKEN with actual token)
curl -X POST http://localhost:5000/api/v1/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "title": "Beautiful Beach House",
    "price": 150,
    "latitude": 25.7617,
    "longitude": -80.1918
  }'
```

## Feature Testing Checklist

### ✅ Index Page (`index.html`)
- [ ] Places load correctly
- [ ] Price filter works
- [ ] Login/Logout button shows correctly
- [ ] "View Details" links work
- [ ] Responsive design on mobile

### ✅ Login Page (`login.html`)
- [ ] Form validation works
- [ ] Successful login redirects to index
- [ ] Error messages display for invalid credentials
- [ ] JWT token stored in cookie

### ✅ Place Details (`place.html`)
- [ ] Place information displays correctly
- [ ] Reviews show (if any exist)
- [ ] "Add Review" button appears for logged-in users
- [ ] "Add Review" link goes to correct page

### ✅ Add Review (`add_review.html`)
- [ ] Redirects to index if not logged in
- [ ] Form validation works
- [ ] Review submission successful
- [ ] Redirects back to place details

## Troubleshooting

### Common Issues

**1. API Connection Failed**
- Ensure API server is running on port 5000
- Check for CORS errors in browser console
- Verify flask-cors is installed: `pip install flask-cors`

**2. Login Not Working**
- Check if user exists in the system
- Verify password is correct
- Check browser console for errors
- Ensure JWT token is being set in cookies

**3. Places Not Loading**
- Check API server is running
- Verify places exist in the system
- Check browser console for errors
- Test API directly: `curl http://localhost:5000/api/v1/places`

**4. Reviews Not Working**
- Ensure user is logged in
- Check JWT token is valid
- Verify place ID is correct in URL
- Check API endpoint: `curl http://localhost:5000/api/v1/places/PLACE_ID/reviews`

### Browser Console Debugging

Open browser Developer Tools (F12) and check:
- **Console**: For JavaScript errors
- **Network**: For API request/response details
- **Application/Storage**: For cookie values

### API Endpoints

The client uses these API endpoints:
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/places` - Get all places
- `GET /api/v1/places/{id}` - Get place details
- `POST /api/v1/places/{id}/reviews` - Add review

## Production Considerations

For production deployment:

1. **Security**: Use HTTPS and secure cookie settings
2. **API URL**: Update `API_BASE_URL` in `scripts.js`
3. **CORS**: Configure CORS for production domain
4. **Error Handling**: Add proper error logging
5. **Performance**: Implement caching and optimization
6. **Validation**: Add client-side form validation

## Development Notes

- All HTML validates against W3C standards
- JavaScript uses modern ES6+ features
- CSS follows responsive design principles
- Error handling implemented throughout
- Loading states and user feedback included