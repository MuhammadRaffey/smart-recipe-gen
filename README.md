# Smart Recipe Generator 🍳

A conversational AI app built with [Chainlit](https://www.chainlit.io/) that generates delicious, halal recipes based on user-provided ingredients. Enjoy a delightful, emoji-rich chat experience with real-time streaming responses!

---

## Features

- **Halal Recipe Generation:** Ensures all suggested recipes use only halal ingredients, with guardrails to prevent non-halal suggestions.
- **Streaming Responses:** Recipes are streamed live, so you see the answer as it's generated.
- **Web Search Tool:** Optionally leverages web search for more creative or up-to-date recipes.
- **Friendly, Emoji-Rich UX:** All messages are enhanced with relevant emojis and clear, friendly language.
- **Powered by OpenAI Agents SDK:** Utilizes the [OpenAI Agents SDK](https://github.com/openai/openai-agents) for agent orchestration, streaming, and guardrails.

---

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- OpenAI API key (for LLM access)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents) (installed automatically via `pyproject.toml`)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/MuhammadRaffey/smart-recipe-gen
   cd smart-recipe-gen
   ```

2. **Install dependencies (including Chainlit and OpenAI Agents SDK):**

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

## Using Google Gemini as the Model Provider

You can switch the model provider from OpenAI to Google Gemini by following these steps:

1. **Get a Gemini API Key:**

   - Obtain your Gemini API key from Google and add it to your `.env` file:
     ```env
     GEMINI_API_KEY=your-gemini-api-key
     ```

2. **Update `setup_config.py`:**
   Replace the OpenAI client and model setup with the following code:

   ```python
   import os
   from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

   gemini_api_key = os.getenv("GEMINI_API_KEY")

   # Check if the API key is present; if not, raise an error
   if not gemini_api_key:
       raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

   client = AsyncOpenAI(
       api_key=gemini_api_key,
       base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
   )

   model = OpenAIChatCompletionsModel(
       model="gemini-2.0-flash",
       openai_client=client
   )

   config = RunConfig(
       model=model,
       model_provider=client
   )
   ```

3. **Restart the app:**
   - After making these changes, restart the Chainlit app to use Gemini as the backend.

---

## OpenAI Agents SDK

This project is built on top of the [OpenAI Agents SDK](https://github.com/openai/openai-agents), which provides:

- Agent orchestration and workflow management
- Streaming LLM responses
- Guardrails for input and output validation
- Easy integration with OpenAI models and tools

For more information, see the [OpenAI Agents SDK documentation](https://github.com/openai/openai-agents).

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
- [OpenAI Agents SDK](https://github.com/openai/openai-agents) for agent orchestration and streaming
