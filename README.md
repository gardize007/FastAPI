# 🛍️ FastAPI Marketplace

This project is a full-featured online marketplace built with **FastAPI**, providing users with the ability to post advertisements, communicate with each other, complete transactions, and manage listings in a secure environment.

## 🚀 Features

- ✅ **User Authentication**  
  Register, log in, and log out securely using JWT tokens.

- 📢 **Advertisement Management**  
  Create, edit, view, delete, and mark advertisements as SOLD or RESERVED. Ads include categories and image uploads (up to 5 images each).

- 📸 **Image Handling**  
  Upload, reorder, view, and delete advertisement images with validation and metadata storage.

- 💬 **Messaging System**  
  Real-time communication between buyers and sellers with input validation and user verification.

- 🔍 **Search & Filtering**  
  Search advertisements by keyword and/or category, sort by creation date or user rating.

- ⭐ **User Rating System**  
  Buyers and sellers can rate each other after successful transactions, contributing to user trust.

- 💰 **Transactions**  
  Buyers and sellers can access secure transaction records containing payment and advertisement details.

## 📚 Project Structure

```bash
.
├── app/
│   ├── main.py            # FastAPI app entry point
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── routers/           # API routers
│   └── utils/             # Helper functions and JWT handling
├── uploaded_images/       # Uploaded image directory
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
```

## ✅ User Stories & Acceptance Criteria

The application is built using Agile principles with clearly defined Epics and User Stories. Each function is validated with strict criteria:

- Advertisement CRUD with status control
- Image upload and order handling
- JWT-based user authentication with bcrypt security
- Buyer-seller messaging with validation
- Keyword/category-based search and result sorting by user rating or date
- Per-transaction user rating with strict access control
- Transaction detail visibility with role-based permissions

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Database:** SQLAlchemy + PostgreSQL (or any preferred DB)
- **Auth:** JWT + OAuth2
- **Image Storage:** Local file system
- **Validation:** Pydantic + custom error messages

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/fastapi-marketplace.git
cd fastapi-marketplace

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## 🔐 Security Highlights

- Passwords hashed using bcrypt.
- JWT tokens for user sessions (30-minute expiry).
- Protected routes for authenticated users only.
- Email and password validations for registration and login.

## 📝 License

This project is licensed under the MIT License.