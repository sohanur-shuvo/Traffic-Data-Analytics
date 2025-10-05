# Configuration Guide

## Frontend Configuration

### Environment Variables

The frontend uses environment variables to configure the API endpoint. Create a `.env` file in the `frontend` directory:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:5000/api
```

### Development Setup

1. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. **Default Configuration**:
   - The app will use `http://localhost:5000/api` by default if no `.env` file is present
   - Vite proxy is configured to forward `/api/*` requests to the backend during development

### Production Setup

For production deployments, update the `.env` file with your backend URL:

```bash
VITE_API_BASE_URL=https://your-backend-domain.com/api
```

## Backend Configuration

### API Server Settings

Default configuration in `backend/api.py`:
- **Port**: 5000
- **Host**: 0.0.0.0 (all interfaces)
- **Max Upload Size**: 200MB
- **Allowed File Types**: .xlsx only

### CORS Configuration

CORS is enabled for all origins in development. For production, update `backend/api.py`:

```python
# Production CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

## API Endpoints

All endpoints are prefixed with `/api`:

### 1. Health Check
- **Endpoint**: `GET /api/health`
- **Response**: 
  ```json
  {
    "status": "healthy",
    "message": "Traffic Analytics API is running"
  }
  ```

### 2. File Upload
- **Endpoint**: `POST /api/upload`
- **Content-Type**: `multipart/form-data`
- **Request Body**: 
  - `file`: Excel file (.xlsx)
- **Response**:
  ```json
  {
    "success": true,
    "data": [...],
    "available_dates": ["2024-01-01", "2024-01-02"],
    "total_records": 100,
    "filtered_records": 95,
    "original_records": 100
  }
  ```

### 3. Date Comparison
- **Endpoint**: `POST /api/compare`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "excel_data": [...],
    "date1": "2024-01-01",
    "date2": "2024-01-02",
    "show_highlighted_only": false,
    "min_ratio_threshold": 4
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "comparison_data": [...],
    "summary": {
      "date1": {...},
      "date2": {...},
      "differences": {...}
    },
    "total_slots": 48
  }
  ```

## Troubleshooting

### CORS Errors

**Problem**: Browser blocks requests due to CORS policy

**Solutions**:
1. Ensure backend is running on the correct port (5000)
2. Check that `CORS(app)` is enabled in `backend/api.py`
3. Use Vite proxy during development (already configured)

### Connection Refused

**Problem**: Cannot connect to backend

**Solutions**:
1. Start backend server: `python backend/api.py`
2. Verify backend is running: `curl http://localhost:5000/api/health`
3. Check firewall settings

### API Not Found (404)

**Problem**: API endpoints return 404

**Solutions**:
1. Verify `VITE_API_BASE_URL` includes `/api` suffix
2. Check backend routes are properly registered
3. Ensure both frontend and backend use consistent endpoint paths

### Environment Variables Not Working

**Problem**: `.env` changes not reflected

**Solutions**:
1. Restart Vite dev server after changing `.env`
2. Ensure `.env` file is in `frontend/` directory
3. Verify variable names start with `VITE_` prefix
4. Clear cache: `rm -rf frontend/node_modules/.vite`

## Development Workflow

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   python api.py
   # Server starts on http://localhost:5000
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   # App starts on http://localhost:8080
   ```

3. **Test Connection**:
   - Open browser to http://localhost:8080
   - Upload an Excel file
   - Check browser console for API calls
   - Verify no CORS errors

## Production Deployment

### Backend Deployment

1. Set environment variables:
   ```bash
   export FLASK_ENV=production
   ```

2. Use production WSGI server (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

### Frontend Deployment

1. Create production `.env`:
   ```bash
   VITE_API_BASE_URL=https://api.yourdomain.com/api
   ```

2. Build for production:
   ```bash
   cd frontend
   npm run build
   ```

3. Deploy `dist/` folder to static hosting (Netlify, Vercel, etc.)

### Security Checklist

- [ ] Update CORS origins to whitelist only your frontend domain
- [ ] Enable HTTPS for both frontend and backend
- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Validate and sanitize all inputs
- [ ] Set secure file upload limits
- [ ] Use environment variables for sensitive data
- [ ] Enable error logging and monitoring

