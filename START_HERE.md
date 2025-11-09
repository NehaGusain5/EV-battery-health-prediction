# 🚀 START HERE - How to Run This Project

## ⚠️ Important: You Need to Train the Model First!

The model files (`battery_health_model.pkl`, `feature_scaler.pkl`, `model_info.json`) don't exist yet. You need to train the model first.

## 📋 Quick Start (3 Steps)

### Step 1: Train the Model (Required - First Time Only)

**Option A: Using Jupyter Notebook (Recommended)**

1. Open PowerShell or CMD in this folder
2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   Or if that doesn't work:
   ```cmd
   venv\Scripts\activate.bat
   ```

3. Start Jupyter Notebook:
   ```bash
   jupyter notebook battery_health_modeling.ipynb
   ```

4. In the Jupyter notebook:
   - Click "Cell" → "Run All"
   - Wait for all cells to complete (this may take a few minutes)
   - This will create the model files in your project folder

5. Close Jupyter Notebook when done

**Option B: Quick Check**
- After training, verify these files exist:
  - ✅ `battery_health_model.pkl`
  - ✅ `feature_scaler.pkl`
  - ✅ `model_info.json`

### Step 2: Start Flask API Server

**Open a NEW terminal/PowerShell window:**

1. Navigate to project folder:
   ```powershell
   cd C:\Users\HP\Desktop\EV-battery-health-prediction
   ```

2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Start Flask API:
   ```bash
   python app.py
   ```

4. You should see:
   ```
   ✓ Model loaded successfully
   ✓ Scaler loaded successfully
   Starting Flask server on http://127.0.0.1:5000
   ```

5. **KEEP THIS WINDOW OPEN!** The API must keep running.

### Step 3: Start Streamlit UI

**Open ANOTHER NEW terminal/PowerShell window:**

1. Navigate to project folder:
   ```powershell
   cd C:\Users\HP\Desktop\EV-battery-health-prediction
   ```

2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Start Streamlit:
   ```bash
   streamlit run app_ui.py
   ```

4. Your browser should open automatically at `http://localhost:8501`

5. If it doesn't open, go to: http://localhost:8501

## 🎯 What You Should See

### Terminal 1 (Flask API):
```
============================================================
EV Battery Health Prediction API
============================================================
Loading model and scaler...
✓ Model loaded successfully
Starting Flask server on http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

### Terminal 2 (Streamlit):
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Browser:
- Streamlit app with sliders and buttons
- You can adjust parameters and make predictions!

## 🛠️ Troubleshooting

### Problem: "Model file not found"
**Solution**: You need to train the model first (Step 1)

### Problem: "Module not found"
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "Port already in use"
**Solution**: 
- Close other programs using port 5000 (Flask) or 8501 (Streamlit)
- Or change ports in the code

### Problem: Virtual environment won't activate (PowerShell)
**Solution**: Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

### Problem: Jupyter Notebook won't start
**Solution**: Install Jupyter:
```bash
pip install jupyter
```

## 📝 Summary of Commands

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Install dependencies (if needed)
pip install -r requirements.txt

# 3. Train model (first time only)
jupyter notebook battery_health_modeling.ipynb
# Then: Cell → Run All

# 4. Start Flask API (Terminal 1)
python app.py

# 5. Start Streamlit (Terminal 2 - NEW terminal)
streamlit run app_ui.py
```

## ✅ Checklist

Before running, make sure:
- [ ] Python 3.9+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Model trained (files exist: `battery_health_model.pkl`, `feature_scaler.pkl`, `model_info.json`)
- [ ] Flask API running (Terminal 1)
- [ ] Streamlit UI running (Terminal 2)

## 🎉 You're Ready!

Once both servers are running:
1. Use the Streamlit UI to make predictions
2. Adjust battery parameters with sliders
3. Click "Predict Battery Health"
4. View results, charts, and download PDF reports!

## 📚 Need More Help?

- See `RUN_PROJECT.md` for detailed instructions
- See `QUICK_START.md` for overview
- See `API_USAGE.md` for API documentation
- See `STREAMLIT_USAGE.md` for UI documentation

---

**Remember**: You need **TWO terminal windows** running:
1. Flask API (Terminal 1) - Must stay running
2. Streamlit UI (Terminal 2) - Must stay running

Good luck! 🚀

