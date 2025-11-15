# Getting Started

This document explains what this project does and how anyone can run it locally step by step.

No prior technical or AI knowledge is required.

---

## Overview

This project is a simulated AI-powered customer support assistant.

It behaves like a call center agent that:
- Listens to a customer request
- Understands the intent and details
- Checks basic rules and policies
- Creates a support request
- Produces a clear and structured summary

The system runs completely on your local machine and does not make real phone calls or connect to external services.

---

## What You Will See When It Runs

When the project is running successfully, you will see:
- A conversation between a customer and an AI agent
- A full transcript of the interaction
- A structured summary of the request
- Clear next steps for the customer

This mirrors how real customer support systems work internally.

---

## Requirements

Before starting, ensure you have:
- A computer running Windows, macOS, or Linux
- Python version 3.10 or higher
- Internet access to install dependencies

You do not need:
- Any paid services
- Any API keys
- Any prior AI or programming experience

---

## Step 1: Download the Project

Download or clone the repository to your computer.

Using Git:

    git clone <repository-url>
    cd call-center-ai-assistant


Alternatively, download the ZIP file, extract it, and open a terminal inside the project folder.

---

## Step 2: Set Up the Python Environment

Create a virtual environment:

    python -m venv .venv


Activate the environment.

On Windows:

    .venv\Scripts\activate


On macOS or Linux:

    source .venv/bin/activate


Install the required dependencies:

    pip install -e .[dev]


---

## Step 3: Start the Backend Service

Start the backend service that powers the AI assistant:

    uvicorn app.main:app --reload


If the service starts correctly, open your browser and visit:

    http://127.0.0.1:8000/docs


If this page loads, the backend is running successfully.

---

## Step 4: Start the User Interface

Open a new terminal window while keeping the backend running.

Activate the virtual environment again if needed, then run:

    streamlit run streamlit_app.py


A browser window will open with a simple user interface.

---

## Step 5: Run a Sample Request

In the user interface:
1. Enter a customer name
2. Enter a member ID
3. Enter a request such as:
   Freeze membership for 2 months due to travel
4. Click the Start Call button

The system will process the request automatically.

---

## Understanding the Output

After the request completes, you will see:
- A conversation transcript between the customer and the AI agent
- Extracted structured fields including:
  - Request type
  - Action taken
  - Duration
  - Sentiment
  - Next steps

This is how real customer support systems record and summarize interactions.

---

## Common Issues

If the user interface cannot connect to the backend:
- Ensure the backend service is still running
- Confirm the API base URL is set to http://127.0.0.1:8000

If the application fails to start:
- Verify Python is installed correctly
- Ensure the virtual environment is activated
- Reinstall dependencies using pip install -e .[dev]

---

## Optional Feature

This project includes an optional AI-based extraction mode using a large language model.

This feature is disabled by default and is not required to run the project.

When enabled, it replaces rule-based extraction with AI-driven parsing.

---

## Limitations

This project is a demonstration system:
- All data is stored in memory
- Restarting the application clears all data
- No real phone calls or external systems are used

---

## Intended Audience

This guide is intended for:
- First-time users
- Non-technical reviewers
- Interviewers evaluating the project
- Anyone exploring AI-assisted customer support workflows

---

## Summary

In simple terms, this project demonstrates how an AI assistant can:
- Understand customer requests
- Respond in a natural way
- Follow business rules
- Produce clean and structured summaries

Anyone can run the project locally and understand how AI can support customer service operations.