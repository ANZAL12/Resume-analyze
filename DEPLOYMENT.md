# 🚀 Render Deployment Guide

## 📋 Prerequisites
- GitHub repository with your code
- Render account (free tier available)

## 🔧 Backend Deployment (Python Service)

### 1. Create New Web Service on Render
- **Name**: `resume-analyzer-backend`
- **Runtime**: `Python 3`
- **Build Command**: `cd resume-analyzer/backend && pip install -r requirements.txt`
- **Start Command**: `cd resume-analyzer/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2. Environment Variables (Optional)
```
PYTHON_VERSION=3.9.18
```

### 3. Advanced Settings
- **Auto-Deploy**: Yes (deploys on git push)
- **Branch**: `main`

## 🎨 Frontend Deployment (Static Site)

### 1. Create New Static Site on Render
- **Name**: `resume-analyzer-frontend`
- **Build Command**: `cd resume-analyzer/frontend && npm install && npm run build`
- **Publish Directory**: `resume-analyzer/frontend/build`

### 2. Environment Variables
```
REACT_APP_API_URL=https://your-backend-service.onrender.com
```

### 3. Advanced Settings
- **Auto-Deploy**: Yes
- **Branch**: `main`

## 🔗 Connecting Frontend to Backend

### 1. Update Frontend API URL
In your React app, update the API base URL:

```javascript
// In App.js, replace:
const r = await axios.post("http://127.0.0.1:8000/analyze", fd);

// With:
const r = await axios.post(`${process.env.REACT_APP_API_URL || 'https://your-backend.onrender.com'}/analyze`, fd);
```

### 2. CORS Configuration
The backend already has CORS configured for all origins, which works for production.

## 📁 Required Files

### Backend Files:
```
resume-analyzer/backend/
├── main.py
├── analyzer.py
├── requirements.txt
└── Procfile
```

### Frontend Files:
```
resume-analyzer/frontend/
├── src/
├── public/
├── package.json
└── package-lock.json
```

## 🚀 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy Backend
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure as shown above
5. Click "Create Web Service"

### 3. Deploy Frontend
1. Go to Render Dashboard
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure as shown above
5. Click "Create Static Site"

### 4. Update Frontend Environment
1. In your frontend service settings
2. Add environment variable: `REACT_APP_API_URL=https://your-backend-url.onrender.com`
3. Redeploy the frontend

## 🔧 Troubleshooting

### Common Issues:

1. **Build Fails**: Check Python version compatibility
2. **CORS Errors**: Ensure backend CORS is configured for your frontend URL
3. **File Upload Issues**: Check file size limits (Render has 100MB limit)
4. **Memory Issues**: Upgrade to paid plan if needed

### Debug Commands:
```bash
# Check backend logs
# Go to your backend service → Logs

# Check frontend build
# Go to your frontend service → Logs
```

## 💰 Cost Considerations

### Free Tier Limits:
- **Backend**: 750 hours/month (enough for small projects)
- **Frontend**: Unlimited static sites
- **File Size**: 100MB limit per file

### Paid Plans:
- **Starter**: $7/month for always-on backend
- **Standard**: $25/month for better performance

## 🔒 Security Notes

1. **Environment Variables**: Never commit API keys to GitHub
2. **CORS**: Configure specific domains in production
3. **File Upload**: Consider adding file size and type validation
4. **Rate Limiting**: Consider implementing rate limiting for production

## 📊 Monitoring

### Render Dashboard:
- Monitor service health
- View logs in real-time
- Check resource usage
- Monitor uptime

### Performance:
- Backend response times
- Frontend load times
- Error rates
- Resource utilization

## 🎯 Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables configured
- [ ] CORS properly configured
- [ ] File upload working
- [ ] All API endpoints responding
- [ ] Error handling working
- [ ] Logs accessible

## 🆘 Support

If you encounter issues:
1. Check Render service logs
2. Verify environment variables
3. Test API endpoints manually
4. Check CORS configuration
5. Contact Render support if needed

---

**Your Resume Analyzer will be live at:**
- Frontend: `https://your-frontend-name.onrender.com`
- Backend: `https://your-backend-name.onrender.com`
- API Docs: `https://your-backend-name.onrender.com/docs`
