# Muse Observatory

Muse Observatory is a web application designed to inspire creativity and foster community engagement through daily rotating themes. The application is available at [https://muse-observatory.xyz](https://muse-observatory.xyz).

## Overview

Muse Observatory serves as a platform for exploration and collaboration centered around the cocoex community. It features a daily rotating "Muse" system that presents users with themed inspiration, information, and collaborative opportunities.

## Core Functionality

- **Daily Muse System**: Automatically rotates through seven unique themes (Lunes, Ares, Rabu, Thunor, Shukra, Dosei, Solis), each associated with specific colors, celestial bodies, and social causes.
- **Content Generation**: Provides daily facts and thought-provoking questions related to the current muse theme.
- **Project Collaboration**: Enables users to discover and share projects aligned with the current theme.
- **Responsive UI**: Features a themed user interface that adapts to each day's muse, with dynamic visual elements.

## Technical Architecture

### Backend Technology
- **Python**: Core application language with FastAPI and NiceGUI for the UI framework
- **TinyDB**: Lightweight JSON document database for storing facts, inspirations, and project data
- **OpenAI Integration**: For generating theme-relevant content
- **Rate Limiting**: Implemented with slowapi to manage API usage

### Deployment Infrastructure
- **Docker**: Containerized application with separate services:
  - Main application service
  - Fact generation scheduler
  - NGINX reverse proxy for SSL termination and routing

### System Requirements
- Docker and Docker Compose for containerized deployment
- OpenAI API key (for content generation features)

## Installation & Deployment

1. Clone the repository:
   ```sh
   git clone https://github.com/username/muse-observatory.git
   cd muse-observatory
   ```

2. Configure environment variables (create a .env file):
   ```
   OPENAI_API_KEY=your_openai_api_key
   ENVIRONMENT=production
   ```

3. Launch with Docker Compose:
   ```sh
   docker-compose up --build
   ```

4. Access the application at [http://localhost:8080](http://localhost:8080) (or your configured port)

## API Endpoints

- `/api/health`: Health check endpoint
- `/api/info`: Application information
- `/api/stats`: Usage statistics
- `/observatory`: Main application interface

## About cocoex

[cocoex](http://cocoex.xyz) is a community platform focused on integrating art with impactful social change. The organization brings together artists, creators, and collectors to support and inspire each other while creating a sense of unity and shared purpose.

## Privacy Policy

Muse Observatory collects minimal user data, limited to what's necessary for core functionality. All user inputs and project inspirations are stored securely and used exclusively for enhancing collaborative experiences. No data is sold or shared with third parties.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. Please open issues or pull requests to help improve the project.
