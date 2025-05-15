# Mental Health FAQ Chatbot

A full-stack AI-powered chatbot designed to provide accurate information about mental health topics by matching user questions with pre-defined FAQs using semantic similarity.

![Mental Health Chatbot](https://github.com/kushalr7/AI-Chatbot-for-Mental-Health-FAQs/blob/master/images/icon.png)

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [How It Works](#how-it-works)
- [API Documentation](#api-documentation)
- [Data Source](#data-source)
- [Future Improvements](#future-improvements)
- [Medical Disclaimer](#medical-disclaimer)
- [License](#license)

## Project Overview

This application uses natural language processing techniques to match user queries with mental health FAQs. It leverages Sentence-BERT (SBERT) to encode text into semantic embeddings and finds the most similar pre-defined question using cosine similarity, providing relevant answers to users in a user-friendly chat interface.

**Note:** This application is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.

## Features

- **Semantic Search**: Uses Sentence-BERT for understanding the meaning behind questions
- **Real-time Responses**: Provides immediate answers to mental health questions
- **User-friendly Interface**: Clean, responsive chat interface
- **Medical Disclaimer**: Clear indication that responses are not medical advice
- **High Accuracy**: Matches questions based on meaning, not just keywords

## Project Structure

```
project/
│
├── backend/
│   ├── app.py                # Flask API server
│   ├── model_utils.py        # Sentence-BERT model functionality
│   ├── requirements.txt      # Python dependencies
│   └── data/
│       └── faq.csv           # Mental health FAQs dataset
│
└── frontend/
    ├── package.json          # Node.js dependencies
    ├── public/
    │   └── index.html        # HTML entry point
    └── src/
        ├── index.js          # React entry point
        ├── App.js            # Main app component
        ├── App.css           # App styling
        ├── ChatBot.js        # Chatbot component
        └── ChatBot.css       # Chatbot styling
```

## Technologies Used

### Backend
- **Python 3.x**: Core programming language
- **Flask**: Web framework for API endpoints
- **Sentence-Transformers**: For semantic text embeddings
- **scikit-learn**: For cosine similarity calculations
- **pandas**: For data handling and manipulation

### Frontend
- **React**: Component-based UI library
- **Axios**: HTTP client for API requests
- **CSS3**: Custom styling

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

### Backend Setup

1. Navigate to the backend directory:

```bash
cd project/backend
```

2. Create and activate a virtual environment:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Flask server:

```bash
python app.py
```

The backend will be running on http://localhost:5000.

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd project/frontend
```

2. Install the required dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The frontend will be accessible at http://localhost:3000.

## How It Works

1. **Initialization**: The backend loads a CSV file containing mental health FAQs and uses Sentence-BERT to create vector embeddings for all questions.

2. **User Interaction**: When a user submits a question through the frontend interface, it's sent to the backend via an API call.

3. **Semantic Matching**:
   - The backend encodes the user's question into a vector embedding
   - Calculates cosine similarity between the user's question embedding and all pre-encoded FAQ questions
   - Finds the most similar question that exceeds a confidence threshold

4. **Response**: The answer corresponding to the best-matched question is returned to the frontend, along with a medical disclaimer.

5. **Display**: The frontend displays the response in the chat interface, preserving the conversation history.

## API Documentation

### `GET /health`
Health check endpoint to verify the server is running.

**Response**:
```json
{
  "status": "healthy"
}
```

### `POST /ask`
Submit a question to the chatbot.

**Request Body**:
```json
{
  "query": "What causes depression?"
}
```

**Response**:
```json
{
  "response": "Depression is caused by a combination of genetic, biological, environmental, and psychological factors...",
  "disclaimer": "Note: This is not medical advice. If you're struggling, please reach out to a licensed mental health professional or helpline.",
  "confidence": 0.89,
  "matched_question": "What causes depression?"
}
```

## Data Source

The application uses a curated CSV file containing frequently asked questions about mental health topics. Each entry includes:
- A unique question ID
- The question text
- The corresponding answer

The data covers various mental health topics, including:
- Common mental health conditions
- Treatment options
- Support resources
- General mental health information

## Future Improvements

- **Multiple Language Support**: Add capability to handle questions in different languages
- **Generative AI Integration**: Incorporate generative models for questions outside the FAQ scope
- **Authentication**: Add admin-only features for FAQ management
- **Rate Limiting**: Implement protection against abuse
- **User Feedback**: Add mechanisms to improve answers based on user feedback
- **Additional Data Sources**: Expand the knowledge base with more mental health resources

## Medical Disclaimer

This chatbot is not a substitute for professional medical advice, diagnosis, or treatment. The information provided is for educational purposes only. If you are experiencing a mental health crisis, please contact a licensed mental health professional, call a crisis hotline, or go to your nearest emergency room.

## License

[MIT License](https://opensource.org/licenses/MIT)
