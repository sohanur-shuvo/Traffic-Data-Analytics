# Traffic Analytics Dashboard - Backend Frontend Connection

This guide shows how to run the Traffic Analytics Dashboard with connected frontend and backend components.

## 🏗️ Architecture

- **Frontend**: React application with TypeScript, Vite, and Tailwind CSS
- **Backend**: Flask API server with pandas and openpyxl for Excel processing
- **Communication**: REST API with JSON over HTTP

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
python start-dev.py
```

This will:
- Check and install backend dependencies
- Check frontend dependencies 
- Start the backend server
- Provide instructions for starting the frontend

### Option 2: Manual Setup

#### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the Flask server:**
   ```bash
   python api.py
   ```
   The API will be available at `http://localhost:5000`

#### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:8080`

## 📡 API Endpoints

### Health Check
- **URL**: `GET /api/health`
- **Response**: `{"status": "healthy", "message": "Traffic Analytics API is running"}`

### File Upload
- **URL**: `POST /api/upload`
- **Content-Type**: `multipart/form-data`
- **Body**: Excel file (.xlsx)
- **Response**: Processed data with available dates

### Data Comparison
- **URL**: `POST /api/compare`
- **Content-Type**: `application/json`
- **Body**: Comparison request with dates and filters
- **Response**: Comparison data and summary statistics

## 🛠️ Development

### Backend Development

The Flask API (`backend/api.py`) provides:
- Excel file processing with pandas
- 15-minute interval generation (8:00 AM - 8:00 PM)
- Date filtering and comparison logic
- Summary statistics calculation

Key features:
- CORS enabled for frontend communication
- File upload with security validation
- Error handling with proper HTTP status codes
- JSON serialization for pandas DataFrames

### Frontend Development

The React frontend uses:
- **API Service** (`frontend/src/services/api.ts`) for backend communication
- **File Uploader** with real API calls instead of client-side processing
- **Comparison Table** that fetches data from backend
- **Summary Totals** using API response data

Key components:
- `FileUploader.tsx` - Handles Excel upload via API
- `ComparisonTable.tsx` - Displays comparison results from API
- `SummaryTotals.tsx` - Shows summary statistics
- `api.ts` - API service layer for HTTP communication

### Configuration

**Backend** (`backend/api.py`):
- Port: 5000
- Max file size: 200MB
- Supported formats: .xlsx only

**Frontend** Configuration:
- Create `frontend/.env` file (copy from `frontend/.env.example`)
- Set `VITE_API_BASE_URL` environment variable
- Default: `http://localhost:5000/api`
- Or run: `python setup-frontend-env.py` for guided setup

**Vite Proxy** (Development):
- API requests to `/api/*` are automatically proxied to `http://localhost:5000`
- No CORS issues during development
- See `frontend/vite.config.ts` for configuration

## 🔍 Troubleshooting

### CORS Issues
If you see CORS errors, ensure:
- Backend is running on port 5000
- CORS is enabled in Flask (`CORS(app)`)
- Frontend makes requests to correct API URL

### File Upload Issues
- Check file size (max 200MB)
- Ensure file is .xlsx format
- Verify backend uploads directory exists

### Connection Issues
- Backend must be running before frontend
- Check that both servers are on expected ports
- Verify network connectivity between frontend and backend

## 📊 Data Flow

1. **Upload**: User uploads Excel file via React frontend
2. **Process**: Frontend sends file to Flask backend via API
3. **Parse**: Backend processes Excel with pandas
4. **Filter**: Data filtered for business hours (8 AM - 8 PM)
5. **Compare**: Frontend requests comparison between selected dates
6. **Display**: Backend returns comparison results and summary stats

## 🎯 Features

- **Real File Processing**: Excel files processed on backend with pandas
- **API-First**: All data operations go through REST API
- **Scalable Architecture**: Frontend and backend can be deployed separately
- **Error Handling**: Proper error responses with meaningful messages
- **Type Safety**: TypeScript interfaces for API communication

## 🔧 Next Steps

- Add authentication/authorization
- Implement data persistence (database/datastore)
- Add more analytics endpoints
- Deploy to production environment
- Add automated testing
