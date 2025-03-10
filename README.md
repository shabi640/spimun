# SPIMUN 2025

> The official platform for St.Peters International Modelling United Nations 2025

[![GitHub issues](https://img.shields.io/github/issues/shabi640/spimun)](https://github.com/shabi640/spimun/issues)
[![GitHub license](https://img.shields.io/github/license/shabi640/spimun)](https://github.com/shabi640/spimun/blob/master/LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Frontend](#running-the-frontend)
  - [Running the Backend](#running-the-backend)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🔍 Overview

SPIMUN 2025 is a comprehensive platform designed for the Shanghai Pinghe International Model United Nations conference. The platform facilitates delegate registration, committee assignments, resolution submissions, and communication between participants.

## ✨ Features

- **Delegate Management**: Register, sign in, and manage delegate profiles
- **Committee System**: Browse and join different UN committees
- **Resolution Submission**: Submit and review resolution papers
- **Real-time Updates**: Get notifications about schedule changes and important announcements
- **Admin Dashboard**: Comprehensive tools for organizers and chairs
- **Responsive Design**: Works on desktops, tablets, and mobile devices

## 🛠️ Tech Stack

### Frontend

- Vue.js 3 with Composition API
- TypeScript
- Vue Router
- Modern CSS with animations and glassmorphism design

### Backend

- Node.js
- Express.js
- MongoDB
- JWT Authentication

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or newer)
- npm or yarn
- MongoDB (for backend)

### Installation

Clone the repository:

```bash
git clone https://github.com/shabi640/spimun.git
cd spimun
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create a .env file for environment variables
cp .env.example .env
```

#### Backend Setup

```bash
# Navigate to backend directory
cd ../backend

# Install dependencies
npm install

# Create a .env file for environment variables
cp .env.example .env
```

Update the `.env` files in both directories with your specific configurations.

#### Environment Variables

For security reasons, sensitive data like API keys and secret tokens are stored in environment variables. The repository includes `.env.example` files that show the required variables without exposing actual values.

Important environment variables:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key for AI formatting features
- `JWT_SECRET_KEY`: Secret key for JWT token generation

To set up:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your actual values
nano .env
```

⚠️ Never commit your actual `.env` file to version control!

## 💻 Usage

### Running the Frontend

```bash
# From the frontend directory
npm run dev

# Or to build for production
npm run build
```

The frontend development server will start at `http://localhost:5173` (or another port if 3000 is in use).

### Running the Backend

```bash
# From the backend directory
npm run dev

# Or to run in production mode
npm start
```

The backend API will be available at `http://localhost:8000` by default.

## 📱 Screenshots

![Home Page](https://via.placeholder.com/800x450) <!-- Replace with actual screenshot -->
![Dashboard](https://via.placeholder.com/800x450) <!-- Replace with actual screenshot -->

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the [MIT License](LICENSE) - a permissive license that allows you to:

- ✅ Use the software commercially
- ✅ Modify the software
- ✅ Distribute the software
- ✅ Use and modify the software privately

The only requirement is to include the original copyright and license notice in any copy of the software/source.

See the [LICENSE](LICENSE) file for the full text of the license.

## 📬 Contact

Project Link: [https://github.com/shabi640/spimun](https://github.com/shabi640/spimun)

---

⭐ Star us on [GitHub](https://github.com/shabi640/spimun) — it helps!
