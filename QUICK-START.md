# Quick Start Guide

Get your Traffic Analytics Dashboard up and running in 3 simple steps!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Terminal/Command Prompt access

## Step 1: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask API server
python api.py
```

The backend API will start on `http://localhost:5000`

You should see:
```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

**Keep this terminal window open!**

## Step 2: Setup Frontend

Open a **new terminal window** and run:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies (first time only)
npm install

# Configure environment (first time only)
# Option A: Use setup script
python ../setup-frontend-env.py

# Option B: Manual setup
cp .env.example .env
# Edit .env if needed (default settings work for local development)

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:8080`

You should see:
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:8080/
➜  Network: use --host to expose
```

## Step 3: Test the Application

1. **Open your browser**: Navigate to `http://localhost:8080`

2. **Upload Excel file**: 
   - Click or drag & drop your `.xlsx` file
   - File should contain date/time and customer in/out data

3. **View data**: The app will display:
   - Available dates in your data
   - Data preview table

4. **Compare dates**:
   - Select two dates from the dropdowns
   - Adjust filters (ratio threshold, show highlighted only)
   - View comparison results and summary totals

## Verify Installation

Run the automated test script:

```bash
# From the project root directory
python test-api-connection.py
```

This will test:
- ✅ Backend health check
- ✅ Upload endpoint availability
- ✅ Compare endpoint availability
- ✅ Frontend configuration

## Common Issues & Solutions

### Issue: "Cannot connect to backend"

**Solution**:
1. Make sure backend is running in another terminal
2. Check if port 5000 is already in use
3. Run: `python backend/api.py`

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "npm: command not found"

**Solution**:
1. Install Node.js from: https://nodejs.org/
2. Restart your terminal
3. Verify: `node --version` and `npm --version`

### Issue: CORS errors in browser console

**Solution**:
1. Backend should be running on port 5000
2. Frontend proxy is configured (check `vite.config.ts`)
3. Restart both servers

### Issue: ".env file not found" warning

**Solution**:
```bash
# Run setup script
python setup-frontend-env.py

# Or manually create
cd frontend
cp .env.example .env
```

## File Format Requirements

Your Excel file should contain:
- **Date column**: Date values (e.g., 2024-01-01)
- **Time column**: Time values or timestamp
- **Customer In column**: Numeric values
- **Customer Out column**: Numeric values

Example structure:
```
| Store | Zone | Traffic Start TS      | Duration | Customer In | Customer Out |
|-------|------|-----------------------|----------|-------------|--------------|
| A     | 1    | 2024-01-01 08:00:00   | 15       | 25          | 22           |
| A     | 1    | 2024-01-01 08:15:00   | 15       | 30          | 28           |
```

## Next Steps

- 📖 Read [CONFIGURATION.md](CONFIGURATION.md) for advanced setup
- 📖 Read [README-API.md](README-API.md) for API documentation
- 🔧 Customize settings in frontend `.env` file
- 🚀 Deploy to production (see CONFIGURATION.md)

## Need Help?

1. Check [CONFIGURATION.md](CONFIGURATION.md) for detailed setup
2. Run `python test-api-connection.py` to diagnose issues
3. Check browser console for frontend errors
4. Check terminal output for backend errors

## Development Workflow

**Terminal 1 (Backend)**:
```bash
cd backend
python api.py
# Leave running
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
# Leave running
```

**Terminal 3 (Testing/Commands)**:
```bash
# Use for testing, git commands, etc.
python test-api-connection.py
```

---

**Ready to go!** 🚀 Open http://localhost:8080 and start analyzing your traffic data!

