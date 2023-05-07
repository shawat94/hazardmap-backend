HazardMap is a basic geospatial web application which allows users to place ‘hazard pins’ on a map, which can be removed as they are resolved. Technologies utilized include:

Database Layer:
- PostgreSQL (with PostGIS extension)

API Layer:
- Flask
- SQLAlchemy (incl. GeoAlchemy)
- JWT and BCrypt for user authentication
- Shapely for spatial data conversions
- Alembic (DB version control)

Frontend Layer:
- React.js
- Material UI as styling framework
- React-Redux for state management (with some use of useState hook)
- MapLibre for frontend map engine (with react-map-gl as a wrapper for state management)
- MapTiler as basemap service