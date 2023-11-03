# Advanced Documentation

This documentation provides more information about the development process of this project.

## Tools

This project is developed by the most recent and famous tools of the tech world.

- **PostgreSQL**: Fast and reliable database for hight amount of read and writes.
- **FastAPI**: For developing fast RESTful APIs on top of asynchronous structure.
- **Pydantic**: For fast data validation based on the pre-defined schemas.
- **Tortoise-ORM**: An ORM with similar API to the Django ORM. To easily work with the database. It supports asynchronous.
- **Aerich**: A migration manager that supports tortoise-orm.
- **G4F**: GPT4Free library to use compatibility of the LLM models for free. It supports almost all recent LLM models such as GPT3.5 and GPT4.
- **Black**: To auto-format the code based on the PEP8 code style.
- **Isort**: To sort the imports in modules based on the standards of Python.

## System Design

The code includes these main parts:

- **Settings**: All settings needed to run the app.
- **Main**: Implementation of FastAPI app and endpoints.
- **Models**: Implementation of ORM models.
- **Schemas**: Implementation of input/output schema classes that validates the input data of endpoints and serializes the data for output.
- **Enums**: Defined enumerations.
- **Utils**: Utility functions that can be used in the main operations. Such as AI tools, etc.

## AI Model

This project uses [G4F](https://pypi.org/project/g4f/) library for generating the response for user queries. This library supports almost all LLM provides such as OpenAPI, Bing, ChatGPTX, You, etc.
It also can find the best provider due to choosen LLM model.

In this project we haven't set a static provider and model for the response generator. But we let the user to choose it's LLM model and the g4f will find best provider of that model.
