# Travel Itinerary Management Software

This software manages travel itineraries, including transportation, accommodations, meals, sightseeing activities, and pricing for multiple destinations. This version includes multi-currency support for different destinations.

## Setup and Running the Application

This project is a full-stack application with a Python/Flask backend and a React frontend. You will need to run both servers simultaneously.

### 1. Backend Setup

The backend server is responsible for serving data from the database.

**A. Install Dependencies:**

Navigate to the project root and install the required Python packages:
```bash
pip install -r backend/requirements.txt
```

**B. Create and Seed the Database:**

Before running the server, you need to initialize the database and populate it with sample data. The seed script will create an SQLite database file at `backend/instance/database.db` and populate it with currencies, destinations, hotels, and sightseeing spots.
```bash
python backend/seed.py
```
You should see a "Database seeded!" message.

**C. Run the Backend Server:**

Start the Flask server from the project root:
```bash
python backend/app.py
```
The backend server will run on `http://127.0.0.1:5001`.

### 2. Frontend Setup

The frontend is a React application that displays the data from the backend.

**A. Install Dependencies:**

In a separate terminal, navigate into the `frontend` directory and install the required Node.js packages:
```bash
cd frontend
npm install
```

**B. Run the Frontend Server:**

Once the dependencies are installed, start the React development server:
```bash
npm start
```
The frontend server will run on `http://127.0.0.1:3000` and will open automatically in your browser.

### Summary

1.  Run `pip install -r backend/requirements.txt`.
2.  Run `python backend/seed.py`.
3.  Run `python backend/app.py` (and keep it running).
4.  In a new terminal, run `cd frontend && npm install`.
5.  Run `npm start` in the `frontend` directory.
6.  Open `http://localhost:3000` in your browser to see the application.
