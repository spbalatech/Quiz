# Samsung Smart Cafe Thanjavur Quiz

A price guessing quiz application for Samsung Smart Cafe Thanjavur.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Email Configuration

The application sends registration details via email. To set up email functionality:

1. Go to your Google Account settings (https://myaccount.google.com)
2. Enable 2-Step Verification if not already enabled
3. Go to Security > App passwords
4. Click "Select app" and choose "Other (Custom name)"
5. Enter a name for the app (e.g., "Samsung Quiz")
6. Click "Generate"
7. Copy the 16-character password that appears

Then update the `config.py` file with your email settings:
```python
EMAIL_CONFIG = {
    "sender_email": "your-gmail@gmail.com",  # Your Gmail address
    "sender_password": "xxxx xxxx xxxx xxxx", # 16-character app password
    "receiver_email": "admin@example.com",    # Email to receive registrations
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 465
}
```

**Important:** Keep your app password secure and never commit config.py to version control.

## Running the Application

```bash
streamlit run app.py
```

The quiz will be available at http://localhost:8501
