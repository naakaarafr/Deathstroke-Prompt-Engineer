# 🤖Deathstroke Prompt Engineer

A Streamlit-based web application that transforms simple user inputs into advanced, structured, and optimized prompts for large language models (LLMs) such as Google’s Gemini. This tool helps users craft high-quality, self-aware, and meta prompts to maximize the effectiveness of AI-generated responses.

---

## Table of Contents

* [Features](#features)

* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)

* [Usage](#usage)

* [Project Structure](#project-structure)

* [Configuration](#configuration)

* [License](#license)

* [Acknowledgments](#acknowledgments)

---

## Features

* **Prompt Analysis**: Automatically detects the user’s primary goal, tone, style, and constraints.
* **Structured Transformation**: Decomposes raw prompts into context, role, task, constraints, and examples.
* **Meta-Instructions**: Enriches prompts with self-reflection steps and verification checks.
* **Interactive Interface**: Built with Streamlit for live prompt input and immediate transformed output.
* **Environment Configuration**: Uses `python-dotenv` for secure API key management.

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* A Google Cloud project with access to the Generative AI API (Gemini)
* Streamlit installed globally or in a virtual environment

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/naakaarafr/Deathstroke-Prompt-Engineer.git
   cd Deathstroke-Prompt-Engineer
   ```

2. **Set up a virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory and add your Gemini API key:

   ```ini
   GEMINI_API_KEY=your_api_key_here
   ```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

* In your browser, navigate to `http://localhost:8501`.
* Enter your raw prompt in the input box.
* Click **Transform** to generate the meta prompt.
* Copy the resulting prompt to use as a system message for your LLM.

---

## Project Structure

```
ai-prompt-engineer/
├── app.py                 # Streamlit application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not checked into source control)
├── LICENSE                # Project license
└── README.md              # This file
```

---

## Configuration

* **API Key**: Stored as `GEMINI_API_KEY` in your `.env` file.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

* [Streamlit](https://streamlit.io/) for the interactive UI framework.
* [Google Generative AI](https://cloud.google.com/generative-ai) for the Gemini API.
* Inspiration from prompt engineering best practices and communities.
