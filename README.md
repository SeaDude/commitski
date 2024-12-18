# `commitski`

`commitski` is a personal Python-based CLI tool designed to streamline the Git commit process by using Large Language Models (LLMs) to generate concise and descriptive commit messages. It supports both local (`ollama`) and third-party LLMs (e.g., OpenAI, Anthropic) to analyze staged Git changes and suggest commit messages.

---

## **Features**

- **Automatic Commit Message Generation:**
  - Generates a descriptive commit message by analyzing `git diff` outputs.
  - Supports local LLMs via `ollama` and third-party APIs (e.g., OpenAI's GPT, Anthropic's Claude).

- **Local LLM Support:**
  - Default integration with `ollama` to ensure privacy and GPU-accelerated processing on your machine.

- **Third-Party LLM Integration:**
  - Seamless integration with OpenAI and Anthropic APIs using environment variables.

- **Error Handling:**
  - Handles scenarios like no staged changes, LLM timeouts, and unsupported LLM providers with informative logs.

- **Detailed Feedback:**
  - Logs each step of the process, including Git staging, LLM interaction, and Git commands.

- **Human-in-the-Loop**: 
  - User can edit the commit message before its pushed.

---

## **Installation**

### **Prerequisites**

- **Python 3.7+**
- **Git**
- **ollama** (if using local LLMs)
  - [Download Ollama](https://ollama.ai)
  - Ensure `ollama` is properly configured on your system and that the `llama3.2-vision` model is available:
    ```bash
    ollama pull llama3.2-vision
    ```

- **Optional: Third-Party LLM Support**
  - **OpenAI API:** Set up an API key with access to models like `text-davinci-003`.
  - **Anthropic API:** Set up an API key with access to models like `claude-2`.

### **Installation Steps**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-github-handle>/commitski.git
   cd commitski
   ```

2. **Make the Script Executable:**
   ```bash
   chmod +x commitski.py
   ```

3. **Move to a Directory in Your PATH:**
   ```bash
   mv commitski.py ~/.local/bin/commitski
   ```
   - Alternatively, create a symlink from your locally cloned `commitski.py` file to your local `bin` directory: 
       - `ln -s ~/path/to/commitski/commitski.py ~/.local/bin/commitski`

4. **Ensure `~/.local/bin` is in Your PATH:**
   Add this line to your `~/.bashrc` or `~/.zshrc` (if not already present):
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

5. **Reload Your Shell Configuration:**
   ```bash
   source ~/.bashrc
   ```
   Or:
   ```bash
   source ~/.zshrc
   ```

---

## **Usage**

### **Basic Command**

Run the `commitski` tool from any Git repository directory:
```bash
commitski
```

- **What Happens:**
  1. Stages all changes using `git add .`.
  2. Analyzes the staged changes using your chosen LLM.
  3. Generates a commit message and commits the changes.
  4. Pushes the changes to the remote repository.

### **Third-Party LLM Usage**

To specify a third-party LLM provider:
```bash
commitski <provider>
```

- **Examples:**
  - Use OpenAI:
    ```bash
    commitski openai
    ```
  - Use Anthropic:
    ```bash
    commitski anthropic
    ```

### **Example Output**
```plaintext
[2024-12-07 15:00:00] Starting the commit process...
[2024-12-07 15:00:01] Staging all changes...
[2024-12-07 15:00:02] Retrieving git changes...
[2024-12-07 15:00:03] Preparing prompt for Ollama...
[2024-12-07 15:00:04] Sending request to Ollama LLM...
[2024-12-07 15:00:30] Received response from Ollama.
[2024-12-07 15:00:31] Committing changes with message: Update README and FAQ sections.
[2024-12-07 15:00:32] Pushing changes to remote repository...
[2024-12-07 15:00:33] Push completed.
[2024-12-07 15:00:33] Commit process completed successfully.
```

---

## **Configuration**

### **Environment Variables**

To use third-party LLMs, set the following environment variables:

- **OpenAI:**
  ```bash
  export OPENAI_API_KEY=<your_openai_api_key>
  ```

- **Anthropic:**
  ```bash
  export ANTHROPIC_API_KEY=<your_anthropic_api_key>
  ```

To persist these, add them to your shell configuration:
```bash
echo 'export OPENAI_API_KEY=<your_openai_api_key>' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY=<your_anthropic_api_key>' >> ~/.bashrc
source ~/.bashrc
```

---

### Reviewing and Editing the Generated Commit Message

By default, `commitski` now provides an opportunity to review and modify the generated commit message before finalizing the commit:

1. **Edit:** Press `E` to open the commit message in your default editor (defined by the `EDITOR` environment variable). After you close the editor, the modified message will be used for the commit.

2. **Accept:** Press `A` to accept the generated message as-is and proceed with the commit.

3. **Cancel:** Press `C` to abort the commit process altogether.

This ensures you have full control over the final commit message while still leveraging the power of LLMs to generate a suitable starting point.

## **FAQs**

### 1. **What happens if there are no changes to commit?**
The tool will detect this and exit with the message:
```plaintext
Error: No changes to commit.
```

### 2. **What if `ollama` is not installed?**
Ensure you have `ollama` installed and a model downloaded then set the `OLLAMA_MODEL` variable in `commitski.py`.

### 3. **How does the tool interact with third-party LLMs?**
Third-party LLMs like OpenAI and Anthropic require valid API keys, which you must set as environment variables. The tool uses their APIs to process prompts and return commit messages.

### 4. **Can I customize the LLM prompt?**
Yes, you can edit the `PROMPT` variable in `commitsky.py`.

---

## **Disclaimer**

`commitski` is provided **as-is** and intended for **personal and non-commercial use** only. It is not designed, tested, or recommended for production environments or critical workflows.

By using this tool, you acknowledge and agree that:

- Any outputs (including commit messages) are generated by external Large Language Models (LLMs) and may contain inaccuracies, errors, or unintended content.
- You assume all responsibility and risk for any actions taken based on the output of `commitski`.
- The author(s) and contributors shall not be held liable for any damages, losses, or issues arising from the use or misuse of this tool.

Use at your own discretion and always review commit messages before finalizing.

## **License**

This project is licensed under the [MIT License](LICENSE).
