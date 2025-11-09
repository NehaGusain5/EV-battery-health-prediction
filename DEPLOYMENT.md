# Deployment Instructions

This guide provides step-by-step instructions for deploying the EV Battery Health Prediction application to Streamlit Cloud or Render.

## Table of Contents

1. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
2. [Render Deployment](#render-deployment)
3. [Environment Variables](#environment-variables)
4. [Troubleshooting](#troubleshooting)

## Streamlit Cloud Deployment

### Prerequisites

1. GitHub account
2. Repository with your code pushed to GitHub
3. Streamlit Cloud account (free tier available)

### Step-by-Step Instructions

#### 1. Prepare Your Repository

Ensure your repository structure includes:
```
EV-battery-health-prediction/
├── app_ui.py
├── app.py
├── requirements.txt
├── battery_health_model.pkl
├── feature_scaler.pkl
├── model_info.json
├── data/
│   └── merged_battery_data.csv
└── README.md
```

#### 2. Create Streamlit Configuration

Create a `.streamlit/config.toml` file (if not exists):
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

#### 3. Create `packages.txt` (Optional)

If you need system packages, create `packages.txt`:
```
# Add system packages if needed
```

#### 4. Deploy to Streamlit Cloud

1. **Sign up for Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Sign up with your GitHub account

2. **Create New App**:
   - Click "New app" button
   - Select your GitHub repository
   - Choose branch (usually `main` or `master`)
   - Set main file path: `app_ui.py`

3. **Configure App Settings**:
   - **App URL**: Choose a unique URL
   - **Python version**: 3.9 or higher
   - **Advanced settings**: Configure if needed

4. **Set Environment Variables**:
   - Go to "Advanced settings" → "Secrets"
   - Add the following secrets:
     ```toml
     OPENAI_API_KEY=your-openai-api-key-here
     FLASK_API_URL=https://your-flask-api-url.herokuapp.com
     ```

5. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at `https://your-app-name.streamlit.app`

### Important Notes for Streamlit Cloud

- **Flask API**: Streamlit Cloud hosts only the Streamlit app. You need to deploy the Flask API separately (see Render deployment below)
- **Model Files**: Ensure model files are committed to the repository (consider using Git LFS for large files)
- **Data Files**: Include data files in the repository or use external storage

### Streamlit Cloud Limitations

- No persistent storage
- 1 GB memory limit (free tier)
- App sleeps after inactivity (free tier)
- No background tasks

## Render Deployment

### Deploying Flask API to Render

#### 1. Prepare for Deployment

Create a `render.yaml` file in your project root:
```yaml
services:
  - type: web
    name: battery-health-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
    disk:
      name: battery-health-disk
      mountPath: /opt/render/project/src
      sizeGB: 1
```

#### 2. Deploy to Render

1. **Sign up for Render**:
   - Go to https://render.com
   - Sign up with GitHub account

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure settings:
     - **Name**: `battery-health-api`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`

3. **Set Environment Variables**:
   - Add environment variables in Render dashboard:
     - `PYTHON_VERSION=3.9.0`
     - (No API keys needed for Flask API)

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment
   - Your API will be at `https://battery-health-api.onrender.com`

5. **Update Streamlit App**:
   - Update `FLASK_API_URL` in Streamlit Cloud secrets to your Render API URL

### Alternative: Deploy Flask API to Heroku

#### 1. Install Heroku CLI

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create Heroku App

```bash
heroku login
heroku create battery-health-api
```

#### 3. Create `Procfile`

Create `Procfile` in project root:
```
web: python app.py
```

#### 4. Create `runtime.txt`

Create `runtime.txt`:
```
python-3.9.0
```

#### 5. Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### 6. Set Environment Variables (if needed)

```bash
heroku config:set FLASK_ENV=production
```

## Environment Variables

### Required Environment Variables

| Variable | Description | Where to Set |
|----------|-------------|--------------|
| `OPENAI_API_KEY` | OpenAI API key for AI insights | Streamlit Cloud secrets |
| `FLASK_API_URL` | Flask API URL | Streamlit Cloud secrets |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Port for Flask API | `5000` |

## Complete Deployment Architecture

```
┌─────────────────────┐
│  Streamlit Cloud    │
│  (app_ui.py)        │
│  User Interface     │
└──────────┬──────────┘
           │
           │ HTTP Requests
           │
┌──────────▼──────────┐
│  Render/Heroku      │
│  (app.py)           │
│  Flask API          │
│  ML Model           │
└─────────────────────┘
```

## Deployment Checklist

### Before Deployment

- [ ] All dependencies in `requirements.txt`
- [ ] Model files committed to repository
- [ ] Environment variables documented
- [ ] API URL configured correctly
- [ ] Error handling implemented
- [ ] Testing completed locally

### Streamlit Cloud

- [ ] Repository pushed to GitHub
- [ ] `app_ui.py` is the main file
- [ ] Environment variables set in secrets
- [ ] Flask API URL configured
- [ ] Model files accessible

### Flask API (Render/Heroku)

- [ ] `app.py` configured for production
- [ ] Model files included
- [ ] Port configuration correct
- [ ] Health check endpoint working
- [ ] CORS configured (if needed)

## Troubleshooting

### Streamlit Cloud Issues

**Issue: App won't start**
- Check logs in Streamlit Cloud dashboard
- Verify `app_ui.py` is the correct main file
- Check for import errors

**Issue: Cannot connect to Flask API**
- Verify `FLASK_API_URL` is set correctly
- Check Flask API is deployed and running
- Test API endpoint manually

**Issue: Model files not found**
- Ensure files are committed to repository
- Check file paths are correct
- Consider using Git LFS for large files

### Render/Heroku Issues

**Issue: Build fails**
- Check `requirements.txt` for all dependencies
- Verify Python version compatibility
- Check build logs for errors

**Issue: App crashes on startup**
- Check logs: `heroku logs --tail` or Render logs
- Verify model files are included
- Check port configuration

**Issue: API timeout**
- Increase timeout in Render/Heroku settings
- Optimize model loading
- Consider using model caching

## Production Best Practices

1. **Security**:
   - Never commit API keys to repository
   - Use environment variables for secrets
   - Enable HTTPS (automatic on Streamlit Cloud/Render)

2. **Performance**:
   - Enable caching (`@st.cache_data`)
   - Optimize model loading
   - Use CDN for static assets

3. **Monitoring**:
   - Set up error logging
   - Monitor API usage
   - Track performance metrics

4. **Scaling**:
   - Use Render/Heroku auto-scaling
   - Consider caching strategies
   - Optimize database queries (if applicable)

## Cost Estimation

### Streamlit Cloud
- **Free Tier**: Unlimited apps, 1 GB memory
- **Team Tier**: $20/month per user

### Render
- **Free Tier**: 750 hours/month, spins down after inactivity
- **Starter**: $7/month, always on

### Heroku
- **Free Tier**: Discontinued (use Render instead)
- **Basic**: $7/month

## Support

For deployment issues:
1. Check deployment logs
2. Review error messages
3. Consult platform documentation
4. Check GitHub issues

## Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Render Documentation](https://render.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com/)

