# Ngao (GitHub PR Triage Bot)







Ngao is a simple Flask-based webhook server designed to automate GitHub Pull Request triage. It helps prevent AI-generated spam by automatically commenting on new PRs 


and requesting human verification (e.g., via Nostr or Proof-of-Work).

## Features

- Listens for GitHub `pull_request` events.


- 
- 
- Verifies webhook signatures for security.
- Automatically adds a "pending-verification" label to new PRs.
- Posts a customizable comment requesting human verification.

## Prerequisites

- Python 3.10+
- A GitHub Personal Access Token (PAT) with `repo` permissions.
- A public-facing URL (or use a tool like `ngrok` for local development).

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ochola-rich/ngao.git
   cd ngao
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up environment variables:**
   Edit the `.env` file and provide your GitHub token and a secret for the webhook.
   ```bash
   GITHUB_TOKEN="your_github_personal_access_token"
   WEBHOOK_SECRET="your_chosen_webhook_secret"
   ```

2. **GitHub Webhook Setup:**
   - Go to your GitHub repository settings.
   - Navigate to **Webhooks** > **Add webhook**.
   - **Payload URL:** `http://your-domain.com/webhook` (or your ngrok URL).
   - **Content type:** `application/json`.
   - **Secret:** Use the same `WEBHOOK_SECRET` defined in your `.env`.
   - **Which events?** Select "Let me select individual events" and check **Pull requests**.
   - Click **Add webhook**.

## Running the Project

1. **Activate the environment (if not already):**
   ```bash
   source venv/bin/activate
   ```

2. **Start the Flask server:**
   ```bash
   python main.py
   ```
   The server will start on `http://0.0.0.0:5000`.

## License

MIT
