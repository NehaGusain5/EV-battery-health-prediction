# AI Insights Setup Guide

This guide explains how to set up and use the AI-generated insights feature in the Streamlit app.

## Overview

The AI insights feature provides intelligent, human-friendly analysis of battery health predictions using:
1. **OpenAI GPT-4** (Primary - Recommended)
2. **HuggingFace** (Fallback - Rule-based)

## Setup Options

### Option 1: OpenAI GPT-4 (Recommended)

#### Step 1: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (starts with `sk-`)

#### Step 2: Install OpenAI Library

```bash
pip install openai
```

#### Step 3: Configure API Key

**Method A: Environment Variable (Recommended)**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Windows (CMD)
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

**Method B: Streamlit UI**
1. Open the Streamlit app
2. Go to sidebar → "🤖 AI Insights Configuration"
3. Select "OpenAI (GPT-4)" from dropdown
4. Paste your API key in the "OpenAI API Key" field

#### Step 4: Use the Feature

1. Select "OpenAI (GPT-4)" as the AI provider
2. Enter your API key (if not set as environment variable)
3. Click "Predict Battery Health"
4. AI insights will be generated automatically

### Option 2: HuggingFace (Fallback)

#### Step 1: Install Dependencies

```bash
pip install transformers torch
```

#### Step 2: Use the Feature

1. Select "HuggingFace" as the AI provider
2. Click "Predict Battery Health"
3. AI insights will be generated (first run may take longer to load the model)

**Note**: HuggingFace uses rule-based insights (not actual AI generation) as a lightweight fallback option.

### Option 3: Disable AI Insights

1. Select "Disabled" from the AI provider dropdown
2. Only standard recommendations will be displayed

## Features

### OpenAI GPT-4 Insights

- **Intelligent Analysis**: Uses GPT-4 to analyze battery parameters and predictions
- **Human-Friendly**: Generates natural language insights
- **Actionable Recommendations**: Provides specific, actionable advice
- **Context-Aware**: Understands relationships between parameters

**Example Output:**
```
🔋 Your battery health is at 65%, which is in the "good" range but showing signs of decline. 
The main factor affecting your battery health is the high temperature (48°C), which accelerates 
degradation. With 850 charging cycles, your battery has experienced moderate wear.

To extend your battery's lifespan, try keeping charging cycles below 600, maintain temperatures 
between 15-35°C, and avoid fast charging when possible. Consider implementing a cooling system 
if high temperatures persist.
```

### HuggingFace Insights

- **Rule-Based**: Uses predefined logic based on battery parameters
- **Fast**: No API calls required
- **Reliable**: Always available (when library is installed)

**Example Output:**
```
🟡 Your battery health is declining at 65.0%. Main contributing factors: high temperature, high cycle count. 
Recommendations: Keep the battery cool (below 35°C) to extend lifespan. With 850 cycles, consider planning 
for battery replacement soon.
```

## Cost Considerations

### OpenAI GPT-4

- **Cost**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **Average Cost per Prediction**: ~$0.01-0.02
- **Free Tier**: $5 credit for new users
- **Recommendation**: Suitable for production use with moderate traffic

### HuggingFace

- **Cost**: Free (runs locally)
- **Resources**: Requires local GPU/CPU for model loading
- **Recommendation**: Good for development/testing

## Troubleshooting

### OpenAI API Errors

**Error: "OpenAI API key required"**
- Solution: Set the API key in environment variable or UI

**Error: "Insufficient quota"**
- Solution: Check your OpenAI account billing and usage limits

**Error: "API request failed"**
- Solution: Check your internet connection and OpenAI API status

### HuggingFace Errors

**Error: "Transformers library not installed"**
- Solution: `pip install transformers torch`

**Error: "Model loading failed"**
- Solution: Check internet connection for first-time model download

**Error: "Out of memory"**
- Solution: Use a smaller model or increase available memory

## Best Practices

1. **API Key Security**: 
   - Never commit API keys to version control
   - Use environment variables for production
   - Rotate API keys regularly

2. **Cost Management**:
   - Monitor OpenAI usage in dashboard
   - Set usage limits if needed
   - Use HuggingFace for development

3. **Performance**:
   - Cache AI insights in session state
   - Use OpenAI for production (faster, better quality)
   - Use HuggingFace for testing (free, local)

## Example Usage

```python
# In Streamlit app
# 1. User selects "OpenAI (GPT-4)"
# 2. Enters API key
# 3. Adjusts battery parameters
# 4. Clicks "Predict Battery Health"
# 5. AI insights are generated and displayed
```

## Support

For issues or questions:
1. Check the [OpenAI API Documentation](https://platform.openai.com/docs)
2. Check the [HuggingFace Documentation](https://huggingface.co/docs/transformers)
3. Review error messages in the Streamlit app
4. Check console logs for detailed error information

## Notes

- AI insights are generated after the prediction is made
- Insights are cached in session state to avoid regeneration
- OpenAI GPT-4 provides better quality insights than HuggingFace
- Both options are optional - the app works without AI insights

