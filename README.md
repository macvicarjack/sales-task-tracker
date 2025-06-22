# Sales Task Tracker

A full-stack web application for outside sales representatives to track and prioritize daily/weekly sales tasks.

## Features

- **Task Management**: Create, view, update, and delete sales tasks
- **Priority Scoring**: Automatic calculation based on days open, revenue potential, and status
- **Filtering**: Filter tasks by status or account
- **Status Tracking**: Mark tasks as open, in-progress, or closed
- **Responsive Design**: Modern UI with Tailwind CSS

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React with TypeScript
- **Styling**: Tailwind CSS
- **Database**: SQLite (local) / PostgreSQL (production)

## Project Structure

```
my-sales-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── vercel.json
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── tailwind.config.js
├── render.yaml
├── railway.json
└── README.md
```

## Quick Start (Local Development)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

### Quick Start Script

Use the provided script to start both servers:
```bash
./start.sh
```

## 🚀 Production Deployment

### Option 1: Render (Recommended - Free Tier)

**Step 1: Deploy Backend**
1. Go to [render.com](https://render.com) and create an account
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `sales-tracker-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

**Step 2: Create Database**
1. Click "New +" → "PostgreSQL"
2. Name it `sales-tracker-db`
3. Copy the connection string

**Step 3: Set Environment Variables**
In your backend service, add:
- `DATABASE_URL`: Your PostgreSQL connection string
- `CORS_ORIGINS`: `https://your-frontend-url.onrender.com`

**Step 4: Deploy Frontend**
1. Click "New +" → "Static Site"
2. Configure:
   - **Name**: `sales-tracker-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Root Directory**: `frontend`
3. Add environment variable:
   - `REACT_APP_API_URL`: `https://your-backend-url.onrender.com`

### Option 2: Vercel

**Backend Deployment:**
1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to backend: `cd backend`
3. Run: `vercel`
4. Set environment variables in Vercel dashboard

**Frontend Deployment:**
1. Navigate to frontend: `cd frontend`
2. Run: `vercel`
3. Set `REACT_APP_API_URL` environment variable

### Option 3: Railway

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect and deploy both services
4. Add PostgreSQL database from the Railway dashboard

### Option 4: Heroku

**Backend:**
1. Create `Procfile` in backend directory:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy using Heroku CLI or GitHub integration

**Frontend:**
1. Use Heroku's static buildpack
2. Set build command: `npm run build`

## Environment Variables

### Backend
```
DATABASE_URL=postgresql://user:password@host:port/database
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend
```
REACT_APP_API_URL=https://your-backend-domain.com
```

## API Endpoints

- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task
- `GET /tasks/{task_id}` - Get a specific task

## Priority Score Formula

The priority score is calculated automatically using:
```
priorityScore = daysOpen * 0.5 + revenuePotential * 0.3 + (status == "open" ? 50 : 0)
```

This formula prioritizes:
- Tasks that have been open longer (50% weight)
- Tasks with higher revenue potential (30% weight)
- Open tasks get a bonus of 50 points

## Daily Usage

Once deployed, you can:
1. **Access your app 24/7** from any device
2. **No need to start servers** - they run automatically
3. **Automatic updates** when you push to GitHub
4. **Database backups** handled by the hosting provider
5. **SSL certificates** included for security

## Cost Estimates

- **Render**: Free tier includes 750 hours/month for web services
- **Vercel**: Free tier includes 100GB bandwidth/month
- **Railway**: Free tier includes $5 credit/month
- **Heroku**: Free tier discontinued, paid plans start at $7/month

## Maintenance

- **Automatic deployments** when you push to GitHub
- **Database backups** handled by hosting provider
- **SSL certificates** automatically managed
- **Monitoring** available through hosting dashboard 