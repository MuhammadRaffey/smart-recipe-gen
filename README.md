# Smart Recipe Generator 🍳

A conversational AI app built with [Chainlit](https://www.chainlit.io/) that generates delicious, halal recipes based on user-provided ingredients. Enjoy a delightful, emoji-rich chat experience with real-time streaming responses!

---

## Features

- **Halal Recipe Generation:** Ensures all suggested recipes use only halal ingredients, with guardrails to prevent non-halal suggestions.
- **Streaming Responses:** Recipes are streamed live, so you see the answer as it's generated.
- **Web Search Tool:** Optionally leverages web search for more creative or up-to-date recipes.
- **Friendly, Emoji-Rich UX:** All messages are enhanced with relevant emojis and clear, friendly language.

---

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- OpenAI API key (for LLM access)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/MuhammadRaffey/smart-recipe-gen
   cd smart-recipe-gen
   ```

2. **Install dependencies:**

   ```sh
   uv sync
   ```

3. **Set up environment variables:**

   - Copy `.env.example` to `.env` and add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your-key-here
     ```

4. **Run the app:**
   ```sh
   uv run chainlit run main.py -w
   ```

---

## Usage

- Start the app and open the provided local URL in your browser.
- You'll be greeted with a friendly welcome message.
- Enter a list of ingredients (e.g., `chicken, rice, tomato`).
- The app will stream a halal recipe, step by step, with chef emojis and clear formatting.
- If you enter a non-halal ingredient, you'll get a clear warning and explanation.

---

## Configuration

- **Halal Guardrails:**
  - The app uses a guardrail agent to check all ingredients for halal compliance.
  - If a non-halal ingredient is detected, the user is notified with a warning emoji and reason.
- **Web Search Tool:**
  - The agent can use a web search tool for more creative or up-to-date recipes.
- **Customizable UX:**
  - All system and error messages use emojis and friendly phrasing for a delightful chat experience.

---

## Contributing

1. Fork the repo and create your feature branch (`git checkout -b feature/your-feature`)
2. Commit your changes (`git commit -am 'Add new feature'`)
3. Push to the branch (`git push origin feature/your-feature`)
4. Open a pull request

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [Chainlit](https://www.chainlit.io/) for the conversational UI framework
- [OpenAI](https://openai.com/) for the LLM backend
