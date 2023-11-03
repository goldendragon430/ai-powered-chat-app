# AI-Powered Chat Application

## Introduction

Welcome to the AI-Powered Chat Application. This application leverages artificial intelligence to enhance the chat experience. You can create interactions with initial prompts and then chat with the AI in chat context.

## Features

- **AI-Driven Conversations**: Utilize advanced natural language processing to understand and respond to user queries.
- **Customizable Responses**: Easily configure the AI to suit the tone and style of your brand or personal preferences. Based on given instructions.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Docker (for containerization)
- Poetry for dependency management

## Installation

To install the AI-Powered Chat Application, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/shahriarshm/ai-powered-chat-app.git
   ```
2. Navigate to the project directory:
   ```sh
   cd ai-powered-chat-app
   ```
3. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

## Configuration

1. Copy the `.env.sample` file to `.env` and fill in the necessary environment variables.
2. Adjust any settings in `src/settings.py` as needed.

## Running the Application

To run the application, execute:

```sh
poetry run python src/main.py
```

Alternatively, you can use Docker:

```sh
docker-compose up --build
```

## Testing

Run the automated tests for this system:

```sh
poetry run pytest
```

## Advanced documentation

You can read the advanced documentation about this project [here](docs/README.md)


## Contributing

Contributions to the AI-Powered Chat Application are welcome. Please adhere to this project's `code of conduct` during your participation.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/shahriarshm/ai-powered-chat-app/blob/main/LICENSE) file for details.
