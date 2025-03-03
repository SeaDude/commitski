#!/home/system9/projects/commitski/.venv/bin/python3

import os
import subprocess
import sys
import tempfile
from datetime import datetime

#==================================================

PROMPT = "Write a short (two sentences max) commit message that encompasses the git diffs shown. Be as succinct, clear and brief as possible. **CRITICAL**: Respond only with the commit message, nothing else."
OLLAMA_MODEL = "deepseek-r1:8b"
OPENAI_MODEL = 'o3-mini'
ANTHROPIC_MODEL = 'claude-3'

#==================================================

def log(message):
    """
    Print a log message with a timestamp.
    """
    print(f"### [{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}] {message}")


def run_command(command, cwd=None, capture_output=False, shell=False):
    """
    Run a shell command and return its output or print errors.
    """
    log(f"Running command: {' '.join(command) if isinstance(command, list) else command}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            shell=shell,
            capture_output=capture_output,
        )
        if capture_output:
            log(f"Command output: {result.stdout.strip()}")
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        log(f"Error: Command failed: {command}\n{e}")
        sys.exit(1)


def is_git_repo():
    """
    Check if the current directory is a Git repository.
    """
    return os.path.isdir(".git")


def stage_changes():
    """
    Stage all changes in the current Git repository.
    """
    log("Staging all changes...")
    run_command("git add .", shell=True)


def get_git_changes():
    """
    Retrieve changes since the last commit.
    """
    log("Retrieving git changes...")
    return run_command("git diff --cached", capture_output=True, shell=True)


def get_commit_summary():
    log("Retrieving commit summary...")
    # Enable capture_output so we get the actual output
    changes = run_command("git status", shell=True, capture_output=True)

    # Now 'changes' is a string containing the output of `git status`
    num_files_changed = len(changes.splitlines())
    num_lines_added = 0
    num_lines_removed = 0

    log(f"Found {num_files_changed} file(s) changed")

    for line in changes.splitlines():
        if "inserted" in line:
            num_lines_added += 1
        elif "deleted" in line:
            num_lines_removed += 1

    summary = f"{num_files_changed} file(s) changed, {num_lines_added + num_lines_removed} lines {'added' if num_lines_added > num_lines_removed else 'removed'}"
    return summary


def ask_ollama(context):
    """
    Use Ollama to generate a commit message based on the context.
    """
    log("Preparing prompt for Ollama...")
    prompt = f"{PROMPT}\n\n{context}"
    
    log("Sending request to Ollama LLM...")
    command = ["ollama", "run", OLLAMA_MODEL]
    response = run_command(command + [prompt], capture_output=True)
    log("Received response from Ollama.")
    return response


def ask_third_party(context, provider):
    """
    Use a third-party LLM (e.g., OpenAI or Anthropic) to generate a commit message.
    """
    log(f"Using third-party provider: {provider}...")
    if provider == "openai":
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        log("Sending request to OpenAI...")
        response = openai.Completion.create(
            model=OPENAI_MODEL,
            prompt = f"{PROMPT}\n\n{context}",
            max_tokens=100,
        )
        log("Received response from OpenAI.")
        return response["choices"][0]["text"].strip()

    elif provider == "anthropic":
        import anthropic
        client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        log("Sending request to Anthropic...")
        response = client.completions.create(
            model=ANTHROPIC_MODEL,
            prompt = f"{PROMPT}\n\n{context}",
            max_tokens_to_sample=100,
        )
        log("Received response from Anthropic.")
        return response.completion.strip()

    else:
        log(f"Error: Unsupported provider '{provider}'.")
        sys.exit(1)


def edit_message_in_editor(initial_message):
    
    # Determine the editor; default to nano
    editor = os.environ.get('EDITOR', 'nano')

    # Create a temporary file to hold the initial message
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:
        tf_name = tf.name
        tf.write(initial_message.encode('utf-8'))

    # Open the editor on the temporary file
    subprocess.call([editor, tf_name])

    # Read the edited message back in
    with open(tf_name, 'r', encoding='utf-8') as f:
        edited_message = f.read()

    # Clean up the temporary file
    os.unlink(tf_name)
    return edited_message.strip()


def commit_changes(message):
    """
    Commit changes to the repository with the provided message and push.
    """
    log(f"Committing changes with message: {message}")
    run_command(f'git commit -m "{message}"', shell=True)
    log("Pushing changes to remote repository...")
    run_command("git push origin main", shell=True)
    log("Push completed.")


def main():
    """
    Main function to handle the commit process.
    """
    log("Starting the commit process...")

    if not is_git_repo():
        log("Error: This directory is not a Git repository.")
        sys.exit(1)

    stage_changes()
    
    summary = get_git_changes()

    provider = sys.argv[1] if len(sys.argv) > 1 else "ollama"

    if provider == "ollama":
        message = ask_ollama(summary)
    else:
        message = ask_third_party(summary, provider)

    # Present the generated message to the user
    print("\nGenerated commit message:\n")
    print(message)
    choice = input("\nDo you want to [E]dit, [A]ccept, or [C]ancel? ").strip().lower()

    if choice.startswith('e'):
        edited_message = edit_message_in_editor(message)
        if not edited_message:
            log("No commit message provided after editing. Aborting.")
            sys.exit(1)
        commit_changes(edited_message)
    elif choice.startswith('a'):
        commit_changes(message)
    else:
        log("Commit canceled by user.")
        sys.exit(0)

    log("Commit process completed successfully.")

if __name__ == "__main__":
    main()
