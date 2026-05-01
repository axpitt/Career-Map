# 🚀 CareerMap AI - Deployment Guide

## Overview

This guide will walk you through deploying CareerMap AI to production. We'll deploy the backend to **Render** and the frontend to **Vercel** for optimal performance and cost-effectiveness.

## Prerequisites

- GitHub account
- OpenAI API key
- Render account (free tier available)
- Vercel account (free tier available)

---

## 1. Backend Deployment (Render)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Production-ready CareerMap AI"
   git push origin main
   ```

2. **Set up environment variables locally**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

### Step 2: Deploy to Render

1. **Go to [Render.com](https://render.com) and sign up/login**

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `career_map_ai` folder (if your repo has multiple projects)

3. **Configure the service**:
   - **Name**: `careermap-ai-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   APP_NAME=CareerMap AI
   DEBUG=false
   LOG_LEVEL=INFO
   SECRET_KEY=your_secret_key_here_generate_a_random_string
   # Optional: enable backend API key auth only if you are not exposing the key in public client code.
   API_KEY=your_api_key_here_for_frontend_authentication
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW_MINUTES=60
   MAX_FILE_SIZE_MB=10
   ```

> Note: For a static frontend hosted on Vercel, avoid embedding the API key directly into browser-side code. Use this value only in a secure server-to-server proxy or internal demo environment.

5. **Deploy**: Click "Create Web Service"

6. **Wait for deployment**: Render will build and deploy your app. This takes 5-10 minutes.

7. **Get your backend URL**: Once deployed, copy the URL (e.g., `https://careermap-ai-backend.onrender.com`)

---

## 2. Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Production

1. **Update the API URL in `frontend/script.js`**:
   ```javascript
   const CONFIG = {
       API_URL: window.location.hostname === 'localhost'
           ? 'http://localhost:8000/analyze'
           : 'https://your-backend-url.onrender.com/analyze', // ← Update this
   ```

   Replace `https://your-backend-url.onrender.com` with your actual Render backend URL.

2. **Commit the changes**:
   ```bash
   git add frontend/script.js
   git commit -m "Update API URL for production"
   git push origin main
   ```

### Step 2: Deploy to Vercel

1. **Go to [Vercel.com](https://vercel.com) and sign up/login**

2. **Import your project**:
   - Click "New Project"
   - Import your GitHub repository
   - Configure project settings:
     - **Framework Preset**: `Other`
     - **Root Directory**: `career_map_ai/frontend`
     - **Build Command**: Leave empty (static site)
     - **Output Directory**: `.` (current directory)

3. **Deploy**: Click "Deploy"

4. **Wait for deployment**: Vercel will deploy your frontend instantly.

5. **Get your frontend URL**: Copy the URL (e.g., `https://careermap-ai.vercel.app`)

---

## 3. Final Configuration

### Update CORS Settings (Optional)

If you want to restrict CORS to only your frontend domain, update the `ALLOWED_ORIGINS` environment variable in Render:

```
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

### Test Your Deployment

1. **Visit your frontend URL**
2. **Upload a resume PDF**
3. **Enter a city**
4. **Click "Analyze My Resume"**
5. **Verify results appear**

---

## 4. Cost Optimization

### Free Tiers
- **Render**: 750 hours/month free
- **Vercel**: Unlimited static sites
- **OpenAI**: Pay per token usage

### Scaling Considerations
- Monitor your Render usage in the dashboard
- If you exceed free limits, consider upgrading to paid plans
- OpenAI costs scale with usage - monitor API usage

---

## 5. Troubleshooting

### Backend Issues
- **Check Render logs**: Go to your service → "Logs" tab
- **Environment variables**: Ensure all required env vars are set
- **OpenAI API key**: Verify it's valid and has credits

### Frontend Issues
- **API URL**: Double-check the URL in `script.js`
- **CORS errors**: Check browser console for CORS issues
- **File uploads**: Ensure files are under 10MB

### Common Errors
- **"Cannot connect to backend"**: Check if Render service is running
- **"Invalid API key"**: Verify OpenAI API key
- **"File too large"**: Check file size limits

---

## 6. Monitoring & Maintenance

### Logs
- **Render**: View logs in dashboard
- **Vercel**: View deployment logs
- **OpenAI**: Monitor usage at platform.openai.com

### Updates
- Push changes to GitHub
- Render/Vercel auto-deploy on main branch pushes
- Test thoroughly before pushing to production

---

## 7. Security Checklist

- ✅ Environment variables configured
- ✅ API keys secured
- ✅ CORS configured
- ✅ Rate limiting enabled
- ✅ File upload validation
- ✅ HTTPS enabled (automatic on Render/Vercel)

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Render/Vercel documentation
3. Check OpenAI API status
4. Ensure all environment variables are set correctly

Your CareerMap AI is now production-ready! 🎉