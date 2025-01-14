# Real Estate Property Listing Platform

## Overview
This Django-based application provides a platform to manage real estate property listings. It supports property listing management, user property portfolios, advanced search and filtering and property shortlisting.

## Features

1. **Property Listing Management**
   - Users can create, update, and delete property listings.
   - Multiple images can be uploaded for each property.

2. **Advanced Search and Filtering**
   - Filter properties by price, city, status, and proximity.
   - Use the Haversine formula to calculate distances for location-based filtering.

3. **User Property Portfolio**
   - Users can view all the properties they own.

4. **Shortlisting Properties**
   - Add properties to a shortlist for quick access.
   - View and remove properties from the shortlist.

5. **Scalability and Efficiency**
   - Efficient search operations and pagination.
   - Dockerize application for easy development and deployment
   - Using Gunicorn to allow Django to handle multiple request at once

---

## Design Explanation

### Goals
- **Efficiency:** Ensure fast search operations using database optimizations.
- **Scalability:** Design the application to handle a growing user base and large datasets.
- **Data Consistency:** Maintain data integrity during concurrent updates.
- **User-Centric Functionality:** Provide features that cater to user needs like shortlisting and detailed filtering.

### Key Components
1. **Property Management:**
   - `PropertyViewSet` handles CRUD operations for properties.
   - Validation ensures only authorized users can update their properties.

2. **Haversine Formula for Distance Calculation:**
   - Calculates the distance between two geographical points.
   - Allows filtering properties within a specified radius.

3. **Pagination:**
   - Implements custom pagination for efficient data display.

4. **Shortlist Management:**
   - Allows users to manage their shortlisted properties.

---

## Implementation Notes

### Efficiency
- Distance calculations are performed at the database level to minimize overhead.
- Indexed queries and pagination improve performance for large datasets.

### Data Consistency
- Validation ensures only property owners can update or delete properties.
- Relationships between models (e.g., Property and PropertyImage) are enforced using foreign keys.

### Scalability
- The modular design supports adding new features like advanced search filters or notifications.
- API design follows REST principles, making it extensible.

---

## API Endpoints

### Property Management
- `GET /properties/` - List properties with filters.
- `POST /properties/` - Create a new property.
- `PUT /properties/<id>/` - Update property details.

### Shortlist Management
- `POST /shortlist/` - Add a property to the shortlist.
- `GET /shortlist/` - View shortlisted properties.
- `DELETE /shortlist/` - Remove a property from the shortlist.

### User Portfolio
- `GET /portfolio/` - View all properties owned by the user.

---

## Validation
- Ensures input values like price and location coordinates are valid.
- Prevents unauthorized updates or deletions.

## Concurrency Handling
- Database transactions and locks are used to handle concurrent updates.

---

## Future Enhancements
- Add support for property recommendations.
- Implement caching for frequently accessed data.
- Integrate real-time notifications for property updates.

---

This application is designed to provide a seamless experience for users while maintaining high performance and scalability.