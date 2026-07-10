
# Yapper Studio

## Description
Yapper Studio is a modern AI chatbot application built with Python, Streamlit, and Google's Gemini 3.5 Flash model. It allows users to chat with different AI personalities in a clean, user-friendly interface.

## Features (Planned)
- Multiple AI personalities to choose from
- Clean and intuitive Streamlit UI
- Real-time chat interaction
- Extensible personality system

## Folder Structure
```
Yapper-Studio/
│
├── app.py                 # Main Streamlit application entry point
├── components/            # Reusable UI components
├── core/                  # Core application logic
├── personalities/         # AI personality definitions
├── styles/                # Application styling files
├── assets/                # Static assets (images, icons, etc.)
├── utils/                 # Utility functions and helpers
├── requirements.txt       # Project dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## Installation Instructions
1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt` (this installs Google's current `google-genai` SDK)
5. Copy `.env.example` to `.env` and add your Gemini API key

## How to Run
1. Ensure your virtual environment is activated
2. Run the Streamlit app: `streamlit run app.py`

## Future Roadmap
- Add more AI personalities
- Implement chat history persistence
- Add customization options for personalities
- Integrate additional AI models
