# 🚀 Deployment Checklist - Sales Task Tracker

## ✅ Step 1: GitHub Setup (5 minutes)
- [ ] Go to [github.com](https://github.com) and sign in
- [ ] Click "+" → "New repository"
- [ ] Name: `sales-task-tracker`
- [ ] Make it **Public**
- [ ] Don't initialize with README
- [ ] Click "Create repository"
- [ ] Copy the repository URL

## ✅ Step 2: Push Code to GitHub
Run these commands in your terminal:
```bash
git remote add origin https://github.com/YOUR_USERNAME/sales-task-tracker.git
git branch -M main
git push -u origin main
```

## ✅ Step 3: Render Backend Deployment (10 minutes)
- [ ] Go to [render.com](https://render.com) and sign up/login
- [ ] Click "New +" → "Web Service"
- [ ] Connect your GitHub repository
- [ ] Configure:
  - **Name**: `sales-tracker-backend`
  - **Environment**: `Python 3`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - **Root Directory**: `backend`
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (green status)

## ✅ Step 4: Create Database (5 minutes)
- [ ] In Render dashboard, click "New +" → "PostgreSQL"
- [ ] Name: `sales-tracker-db`
- [ ] Click "Create Database"
- [ ] Copy the connection string (Internal Database URL)

## ✅ Step 5: Configure Backend Environment Variables
- [ ] Go back to your backend service
- [ ] Click "Environment" tab
- [ ] Add these variables:
  - **Key**: `DATABASE_URL`
  - **Value**: [Your PostgreSQL connection string]
- [ ] Click "Save Changes"
- [ ] Wait for redeployment

## ✅ Step 6: Deploy Frontend (10 minutes)
- [ ] In Render dashboard, click "New +" → "Static Site"
- [ ] Connect the same GitHub repository
- [ ] Configure:
  - **Name**: `sales-tracker-frontend`
  - **Build Command**: `npm install && npm run build`
  - **Publish Directory**: `build`
  - **Root Directory**: `frontend`
- [ ] Click "Create Static Site"
- [ ] Wait for deployment

## ✅ Step 7: Configure Frontend Environment Variables
- [ ] In your frontend service, click "Environment" tab
- [ ] Add:
  - **Key**: `REACT_APP_API_URL`
  - **Value**: `https://sales-tracker-backend.onrender.com`
- [ ] Click "Save Changes"
- [ ] Wait for redeployment

## ✅ Step 8: Update Backend CORS
- [ ] Go back to backend service
- [ ] Add environment variable:
  - **Key**: `CORS_ORIGINS`
  - **Value**: `https://sales-tracker-frontend.onrender.com`
- [ ] Click "Save Changes"

## ✅ Step 9: Test Your App
- [ ] Visit your frontend URL: `https://sales-tracker-frontend.onrender.com`
- [ ] Test creating a new task
- [ ] Test filtering and status changes
- [ ] Check API docs: `https://sales-tracker-backend.onrender.com/docs`

## 🎉 Success!
Your app is now live 24/7! You can:
- Access it from any device
- No need to run commands locally
- Automatic updates when you push code changes
- Database backups handled automatically

## 📱 Your URLs
- **Frontend**: `https://sales-tracker-frontend.onrender.com`
- **Backend API**: `https://sales-tracker-backend.onrender.com`
- **API Documentation**: `https://sales-tracker-backend.onrender.com/docs`

## 💡 Pro Tips
- Bookmark your frontend URL
- The app works on mobile browsers
- You can share the URL with team members
- All data is stored securely in the cloud 