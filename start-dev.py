#!/usr/bin/env python3
"""
Development startup script for Traffic Analytics Dashboard
Starts both Flask backend and provides instructions for frontend
"""

import subprocess
import sys
import os
import threading
import time

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    try:
        os.chdir('backend')
        result = subprocess.run([sys.executable, 'api.py'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Backend error: {result.stderr}")
        else:
            print("✅ Backend started successfully")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")

def check_dependencies():
    """Check and install required dependencies"""
    print("📦 Checking dependencies...")
    
    # Check if backend dir exists
    if not os.path.exists('backend'):
        print("❌ Backend directory not found")
        return False
    
    # Check if frontend dir exists  
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found")
        return False
    
    # Install backend dependencies
    print("📥 Installing backend dependencies...")
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Backend dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False
    
    os.chdir('..')
    
    # Check frontend dependencies
    print("📥 Checking frontend dependencies...")
    os.chdir('frontend')
    if not os.path.exists('node_modules'):
        print("📥 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], check=True, capture_output=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    os.chdir('..')
    return True

def main():
    """Main function"""
    print("🏢 Traffic Analytics Dashboard - Development Setup")
    print("=" * 50)
    
    if not check_dependencies():
        print("❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n🌟 Starting development servers...")
    print("\n📋 To start the frontend:")
    print("   cd frontend")
    print("   npm run dev")
    print("   Then open http://localhost:8080 in your browser")
    
    print("\n🔧 Backend will run on http://localhost:5000")
    print("   API endpoints:")
    print("   - GET  /api/health - Health check")
    print("   - POST /api/upload - Upload Excel file")
    print("   - POST /api/compare - Compare dates")
    
    print("\n⏳ Starting backend server...")
    start_backend()

if __name__ == "__main__":
    main()
