import os
import hmac
import hashlib
import json
from flask import Flask, request, abort
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN environment variable not set.")
    exit(1)
if not WEBHOOK_SECRET:
    print("Error: WEBHOOK_SECRET environment variable not set.")
    exit(1)

g = Github(GITHUB_TOKEN)

def verify_signature(payload_body, signature_header):
    """Verify that the payload was sent from GitHub."""
    if not signature_header:
        return False
    
    # GitHub sends 'sha256=' prefix, remove it
    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False

    mac = hmac.new(WEBHOOK_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    if request.method == 'POST':
        # Verify webhook signature
        signature = request.headers.get('X-Hub-Signature-256')
        if not verify_signature(request.data, signature):
            abort(401, "Signature verification failed.")

        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')

        if event_type == 'pull_request' and payload['action'] == 'opened':
            handle_pull_request_opened(payload)
        
        return 'OK', 200
    else:
        abort(400)

def handle_pull_request_opened(payload):
    repo_name = payload['repository']['full_name']
    pr_number = payload['pull_request']['number']
    pr_url = payload['pull_request']['html_url']
    
    print(f"New PR opened in {repo_name}: #{pr_number} - {pr_url}")

    try:
        repo = g.get_repo(repo_name)
        pull_request = repo.get_pull(pr_number)

        # Add a comment to the PR
        comment_message = (
            "To prevent AI-spam, please sign this message with your Nostr private key "
            "or run this 2-second bash command to solve a PoW token. "
            "Once validated, your PR will be marked as 'verified-human'."
            "\n\n"
            "**[Placeholder for PoW/Nostr verification instructions]**"
        )
        pull_request.create_issue_comment(comment_message)
        print(f"Commented on PR #{pr_number}")

        # Add a label to the PR
        # Check if the label exists, create if not
        label_name = "pending-verification"
        try:
            repo.get_label(label_name)
        except Exception:
            repo.create_label(label_name, "f29513", "Awaiting human verification") # color is a hex code
            print(f"Created label '{label_name}'")
        
        pull_request.add_to_labels(label_name)
        print(f"Added label '{label_name}' to PR #{pr_number}")

    except Exception as e:
        print(f"Error handling PR #{pr_number}: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)