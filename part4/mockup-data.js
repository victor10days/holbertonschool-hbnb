// Comprehensive mockup data for HBnB
const mockupPlaces = [
    {
        id: 'mock-1',
        title: 'Stylish Downtown Loft',
        city: 'New York',
        country: 'United States',
        price_per_night: 125,
        price: 125,
        description: 'Beautiful modern loft in the heart of Manhattan with amazing city views.',
        rating: 4.8,
        reviews_count: 127,
        image_url: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['WiFi', 'Kitchen', 'Air conditioning', 'Heating', 'Workspace'],
        owner: {
            first_name: 'Sarah',
            last_name: 'Johnson'
        },
        reviews: [
            {
                id: 'rev-1',
                text: 'Amazing location and beautiful space! The host was very responsive.',
                rating: 5,
                user: { first_name: 'Michael', last_name: 'Chen' }
            },
            {
                id: 'rev-2', 
                text: 'Great place for a business trip. Very clean and well-equipped.',
                rating: 4,
                user: { first_name: 'Emily', last_name: 'Davis' }
            }
        ]
    },
    {
        id: 'mock-2',
        title: 'Cozy Beach House',
        city: 'Santa Monica',
        country: 'United States',
        price_per_night: 180,
        price: 180,
        description: 'Charming beach house just steps from the ocean with stunning sunset views.',
        rating: 4.9,
        reviews_count: 89,
        image_url: 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['Beach access', 'WiFi', 'Kitchen', 'Parking', 'Hot tub'],
        owner: {
            first_name: 'David',
            last_name: 'Martinez'
        },
        reviews: [
            {
                id: 'rev-3',
                text: 'Perfect beach getaway! The sunsets from the deck are incredible.',
                rating: 5,
                user: { first_name: 'Jessica', last_name: 'Wilson' }
            }
        ]
    },
    {
        id: 'mock-3',
        title: 'Mountain Cabin Retreat',
        city: 'Aspen',
        country: 'United States',
        price_per_night: 95,
        price: 95,
        description: 'Rustic cabin surrounded by nature, perfect for hiking and relaxation.',
        rating: 4.7,
        reviews_count: 156,
        image_url: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['Fireplace', 'WiFi', 'Kitchen', 'Hiking trails', 'Mountain views'],
        owner: {
            first_name: 'Lisa',
            last_name: 'Thompson'
        },
        reviews: [
            {
                id: 'rev-4',
                text: 'So peaceful and relaxing. Great place to disconnect and recharge.',
                rating: 5,
                user: { first_name: 'Robert', last_name: 'Brown' }
            }
        ]
    },
    {
        id: 'mock-4',
        title: 'Historic Townhouse',
        city: 'Boston',
        country: 'United States', 
        price_per_night: 110,
        price: 110,
        description: 'Beautifully restored 19th century townhouse in historic Back Bay.',
        rating: 4.6,
        reviews_count: 203,
        image_url: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['Historic charm', 'WiFi', 'Kitchen', 'Workspace', 'Garden'],
        owner: {
            first_name: 'James',
            last_name: 'Anderson'
        },
        reviews: [
            {
                id: 'rev-5',
                text: 'Beautiful historic home with modern amenities. Perfect location!',
                rating: 4,
                user: { first_name: 'Amanda', last_name: 'Taylor' }
            }
        ]
    },
    {
        id: 'mock-5',
        title: 'Modern City Apartment',
        city: 'Seattle',
        country: 'United States',
        price_per_night: 85,
        price: 85,
        description: 'Sleek modern apartment with city views and easy transit access.',
        rating: 4.5,
        reviews_count: 67,
        image_url: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['City views', 'WiFi', 'Kitchen', 'Gym access', 'Transit nearby'],
        owner: {
            first_name: 'Rachel',
            last_name: 'Kim'
        },
        reviews: [
            {
                id: 'rev-6',
                text: 'Great apartment in a convenient location. Very clean and modern.',
                rating: 5,
                user: { first_name: 'Kevin', last_name: 'Park' }
            }
        ]
    },
    {
        id: 'mock-6',
        title: 'Luxury Penthouse Suite',
        city: 'Miami',
        country: 'United States',
        price_per_night: 250,
        price: 250,
        description: 'Stunning penthouse with panoramic ocean views and private rooftop.',
        rating: 4.9,
        reviews_count: 45,
        image_url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['Ocean views', 'Private rooftop', 'Pool', 'Concierge', 'Luxury finishes'],
        owner: {
            first_name: 'Carlos',
            last_name: 'Rodriguez'
        },
        reviews: [
            {
                id: 'rev-7',
                text: 'Absolutely incredible! The views are breathtaking and the space is luxurious.',
                rating: 5,
                user: { first_name: 'Sofia', last_name: 'Garcia' }
            }
        ]
    },
    {
        id: 'mock-7',
        title: 'Charming Countryside Cottage',
        city: 'Napa Valley',
        country: 'United States',
        price_per_night: 145,
        price: 145,
        description: 'Romantic cottage surrounded by vineyards with wine tasting nearby.',
        rating: 4.8,
        reviews_count: 112,
        image_url: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['Vineyard views', 'Wine tasting', 'Fireplace', 'Garden', 'Hot tub'],
        owner: {
            first_name: 'Michelle',
            last_name: 'Clark'
        },
        reviews: [
            {
                id: 'rev-8',
                text: 'Perfect romantic getaway! The vineyard setting is magical.',
                rating: 5,
                user: { first_name: 'Daniel', last_name: 'White' }
            }
        ]
    },
    {
        id: 'mock-8',
        title: 'Urban Industrial Loft',
        city: 'Portland',
        country: 'United States',
        price_per_night: 75,
        price: 75,
        description: 'Cool industrial loft in trendy arts district with exposed brick.',
        rating: 4.4,
        reviews_count: 89,
        image_url: 'https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
        amenities: ['Exposed brick', 'Arts district', 'WiFi', 'Kitchen', 'Unique design'],
        owner: {
            first_name: 'Tyler',
            last_name: 'Johnson'
        },
        reviews: [
            {
                id: 'rev-9',
                text: 'Super cool space with great character. Love the industrial vibe!',
                rating: 4,
                user: { first_name: 'Megan', last_name: 'Lewis' }
            }
        ]
    }
];

// Function to use mockup data when API fails or for demo purposes
function getMockupPlaces() {
    return mockupPlaces;
}

// Function to get a specific mockup place by ID
function getMockupPlace(id) {
    return mockupPlaces.find(place => place.id === id);
}