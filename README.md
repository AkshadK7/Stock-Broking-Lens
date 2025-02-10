# Stock-Broking-Lens

An AI-powered Visual Search Application for financial enthusiasts to explore the current valuation of brands around them.

## Overview

Stock-Broking-Lens is an innovative application that leverages artificial intelligence to provide users with real-time financial information about various brands. By utilizing visual search capabilities, users can tap into the current valuations and financial data of the brands they encounter in their daily lives.

## Repository Contents

- `backend/`: Contains the backend code and related resources.
- `app.py`: Streamlit application serving as the frontend interface.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `Stock Lens Project Architecture.docx`: Document detailing the project's architecture.
- `README.md`: Project documentation.

## Requirements

- Python 3.x
- Uvicorn
- FastAPI
- Streamlit

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AkshadK7/Stock-Broking-Lens.git
   cd Stock-Broking-Lens
   ```

2. **Install Dependencies**:
   It's recommended to use a virtual environment to manage dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Backend Server**:
   Navigate to the `backend` directory and run:
   ```bash
   uvicorn main:app --reload
   ```

4. **Launch the Frontend Application**:
   In the root directory, execute:
   ```bash
   streamlit run app.py
   ```

## Usage

- **Backend**:
  - The backend is powered by FastAPI and serves as the API layer for the application.
  - Ensure the backend server is running to handle API requests from the frontend.

- **Frontend**:
  - The frontend is built using Streamlit, providing an interactive user interface.
  - Access the application through the URL provided by Streamlit after launching.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/AkshadK7/Stock-Broking-Lens/blob/main/LICENSE) file for details.

Copyright (c) 2024 Akshad Kolhatkar, All Rights Reserved.

## Acknowledgements

Special thanks to the open-source community and contributors for their support and resources.
```

*Note: Ensure that the `requirements.txt` file includes all necessary dependencies for the project. If it doesn't exist, you may need to create it by listing the required packages.* 
