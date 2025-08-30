# ML4TrustworthyReviews

An automated review evaluation system that leverages machine learning and natural language processing to assess review quality, relevance, and credibility for location-based reviews.

Team member: Chelsea Yep

## Quick Start

### Prerequisites
- Python 3.8+
- Git

### Setup and Launch

1. **Clone the repository**
   ```bash
   git clone https://github.com/chelseayep/ML4TrustworthyReviews.git
   cd ML4TrustworthyReviews
   ```

2. **Configure environment variables**
   
   Create a `.env` file in the project root and add your Hugging Face token:
   ```bash
   HF_TOKEN=your_hugging_face_token_here
   ```
   
   > **Note**: A Hugging Face token is required for model inference. Get yours at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

3. **Run the startup script**
   ```bash
   chmod +x startup.sh
   ./startup.sh
   ```

The startup script will automatically:
- Set up the virtual environment
- Install all dependencies
- Configure Python paths
- Launch the Streamlit application

4. **Access the application**
   
   Open your browser and navigate to: `http://localhost:8501`

## Project Structure

```
ML4TrustworthyReviews/
├── startup.sh              # Main startup script - run this to get started
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (create this file)
├── README.md               # This file
├── /src                    # Core source code
│   ├── policies/           # Policy evaluation modules
│   ├── objects.py          # Data structures and models
│   └── ...
├── /streamlit              # Streamlit web application
│   ├── Main.py            # Main dashboard page
│   ├── pages/             # Additional app pages
│   │   ├── testing.py     # Interactive testing interface
│   │   └── ...
├── /workbenches           # Development notebooks and experiments
│   ├── data_processing.ipynb      # Jupyter notebook for processing raw data
│   └── evaluation.ipynb.   # Jupyter notebook for running model on annotated data 
├── /data                  # Data directory
│   ├── raw/              # Original datasets
│   ├── processed/        # Cleaned and processed data
│   └── output/           # Model outputs and results
└── ...
```

## Reproducing Results
To reproduce the model performance metrics shown in the dashboard:

1. Complete the setup following the Quick Start guide above
2. Run the evaluation notebook:
```bash
jupyter notebook workbenches/evaluation.ipynb
```

3. Execute all cells to generate performance metrics on the test dataset

## Features

### Core Functionality
- **Multi-Policy Evaluation**: Detects spam, irrelevant content, and credibility issues
- **Quality Assessment**: Reference metric for review informativeness
- **Interactive Testing**: Real-time evaluation interface
- **Performance Analytics**: Comprehensive model performance dashboard

### Policy Detection
- **Spam/Advertisement**: Rule-based detection of promotional content
- **Relevance**: Context-aware evaluation of business-related content
- **Credibility**: Assessment of genuine user experiences
- **Quality Scoring**: Informative content measurement (reference only)

## Usage

### Web Interface
After running `startup.sh`, access the Streamlit application to:
- View model performance metrics
- Test individual reviews
- Explore violation datasets
- Analyze policy evaluation results

### Development
- **Notebooks**: Explore `/workbenches` for development experiments and analysis
- **Data**: Access raw and processed datasets in `/data`
- **Source Code**: Core logic available in `/src`

## Data Requirements

### Input Format
Reviews should be structured with:
- Review text content
- Numerical rating (1-5)
- Business information (name, description, type)

### Datasets
- **Source**: Google Local Reviews dataset (McAuley Lab, UCSD)
- **Test Data**: 200 manually annotated reviews for validation
- **Output**: Processed violation reports and quality metrics

## Model Performance

### Key Metrics
- **High Recall**: 93-100% across all policy types
- **Moderate Precision**: 53-67% (suitable for first-pass filtering)
- **Overall Accuracy**: 95-99% across different policies

### Best Use Case
Ideal for content moderation workflows with human review, where comprehensive violation detection is prioritized over minimizing false positives.

## Configuration

### Environment Variables
Required in `.env` file:
- `HF_TOKEN`: Hugging Face API token for model access

### Model Configuration
- **Local Models**: Qwen2.5-VL-3B-Instruct, Mistral-7B-Instruct, Gemma-3-1b-it
- **Remote Inference**: Hugging Face Hub integration for testing
- **Device Support**: Automatic MPS/CPU detection for optimal performance


## Troubleshooting

### Common Issues
- **Missing HF_TOKEN**: Ensure `.env` file contains valid Hugging Face token
- **Import Errors**: Verify `startup.sh` completed successfully and added `/src` to path
- **Model Loading**: Check internet connection for initial model downloads
- **Port Conflicts**: Default Streamlit port is 8501, modify if needed


