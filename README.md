# Car Processing System

A comprehensive car data processing system that combines computer vision, natural language processing, and automated email functionality. The system processes car descriptions and images to predict car types, extract structured information using AI, and send detailed reports via email.

## 🚀 Features

- **AI-Powered Car Classification**: Predicts car types from uploaded images
- **Intelligent Information Extraction**: Uses Azure OpenAI to convert natural language car descriptions into structured JSON data
- **Automated Email Reports**: Sends processed car information with attachments via email
- **Web Interface**: User-friendly Gradio-based interface for easy interaction
- **Multi-Provider Email Support**: Compatible with Gmail, Outlook, Hotmail, and Yahoo
- **Structured Data Output**: Converts unstructured car descriptions into organized JSON format

## 🏗️ System Architecture

The system consists of five main components:

1. **CarDataProcessor**: Handles input processing and image management
2. **CarTypePredictor**: Predicts vehicle types from images
3. **CarInformationExtractor**: Extracts structured data using Azure OpenAI
4. **EmailSender**: Manages email delivery with attachments
5. **Gradio Interface**: Provides the web-based user interface

## 📋 Prerequisites

- Python 3.7+
- Azure OpenAI API access
- Email account with app-specific password (recommended for security)

## 🛠️ Installation

### Option 1: Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AI-Powered-Car-Data-Processing-and-Automation-System.git
   cd AI-Powered-Car-Data-Processing-and-Automation-System
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   
   Create a file named `KEY.env` in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
   ```

4. **Configure image path (optional):**
   
   Modify the image path in `car_data_processor.py` if needed:
   ```python
   self.image_path = "your_preferred_path/saved_image.jpg"
   ```

### Option 2: Google Colab

Use the provided `Notebook.ipynb` file:

1. Upload the notebook to Google Colab
2. Run the setup cells
3. Configure the `KEY.env` file as described above
4. Follow the in-notebook instructions

## 🚀 Usage

### Running the Application

```bash
python main.py
```

### Using the Web Interface

1. **Access the interface**: Use the generated public URL ending with `.gradio.live`
2. **Fill in the form**:
   - **Car Description**: Detailed description of the vehicle
   - **Sender Email**: Your email address
   - **Sender Password**: Use an app-specific password (not your regular password)
   - **Receiver Email**: Destination email address
   - **Car Image**: Upload a clear image of the vehicle

3. **Submit and receive results**:
   - Predicted car type
   - Processing time
   - Email delivery status

### Email Security Note

For Gmail users, generate an App Password:
1. Enable 2-Factor Authentication
2. Go to Google Account settings
3. Generate an App Password for "Mail"
4. Use this password instead of your regular Gmail password

## 📊 Output Format

The system generates structured JSON output containing:

```json
{
  "car": {
    "body_type": "SUV",
    "color": "Blue",
    "brand": "Toyota",
    "model": "RAV4",
    "manufactured_year": 2020,
    "motor_size_cc": 2500,
    "tires": {
      "type": "All-Season",
      "manufactured_year": 2019
    },
    "windows": "Tinted",
    "notices": [
      {
        "type": "Maintenance",
        "description": "Recent oil change"
      }
    ],
    "price_or_estimated_price": {
      "amount": 25000,
      "currency": "USD"
    }
  }
}
```

## 📁 Project Structure

```
AI-Powered-Car-Data-Processing-and-Automation-System/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                           # Application entry point
├── car_classifier.py                 # Car type prediction module
├── car_data_processor.py             # Input processing and image handling
├── car_information_extractor.py      # AI-powered information extraction
├── email_sender.py                   # Email functionality
├── Notebook.ipynb                    # Google Colab notebook
├── Solution Design Diagram.drawio    # System architecture diagram
└── Solution Design Diagram.pdf       # Architecture diagram (PDF)
```

## 🔧 Configuration

### Supported Email Providers

| Provider | SMTP Server | Port | Security |
|----------|-------------|------|----------|
| Gmail | smtp.gmail.com | 587 | TLS |
| Outlook/Hotmail | smtp.office365.com | 587 | TLS |
| Yahoo | smtp.mail.yahoo.com | 465 | SSL |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Azure OpenAI API key | Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | Yes |

## 🧪 Example Usage

### Input Example
```
Car Description: "2019 Blue Toyota RAV4 SUV with 45,000 miles, 
all-wheel drive, recently serviced, asking $28,000"

Email: sender@gmail.com
Password: [app-specific-password]
Receiver: buyer@email.com
Image: [uploaded car photo]
```

### Expected Output
- **Predicted Type**: "SUV"
- **Processing Time**: "3.2 seconds"
- **Status**: "Email sent successfully!"

## ⚡ Performance

- **Average Processing Time**: 2-5 seconds
- **Supported Image Formats**: JPG, PNG, JPEG
- **Maximum Image Size**: 10MB (Gradio default)
- **Concurrent Users**: Limited by Gradio's free tier
