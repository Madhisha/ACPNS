const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawnSync } = require('child_process');
const { MongoClient } = require('mongodb');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const PORT = 3000;
const MONGO_URI = 'mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'; // Replace with your MongoDB Cloud URI
const DB_NAME = 'ecampus'; // Replace with your database name
const USERS_COLLECTION = 'users'; // Collection name

let db, usersCollection;

// Initialize the server and connect to MongoDB
MongoClient.connect(MONGO_URI)
  .then((client) => {
    db = client.db(DB_NAME);
    usersCollection = db.collection(USERS_COLLECTION);
    app.listen(PORT, () => {
      console.log('Connected to MongoDB and listening on port', PORT);
      // console.log(`Server running on http://localhost:${PORT}`);
    });
  })
  .catch((error) => console.error('Failed to connect to MongoDB:', error));

// Register route
app.post('/register', async (req, res) => {
  const { rollNo, password } = req.body;

  try {
    // Run the Python script
    const pythonProcess = spawnSync('python', ['login.py', rollNo, password]);

    if (pythonProcess.error) {
      console.error('Error executing Python script:', pythonProcess.error);
      return res.status(500).json({ message: 'Error executing Python script.' });
    }

    const output = pythonProcess.stdout.toString().trim();
    const errorOutput = pythonProcess.stderr.toString().trim();

    if (errorOutput) {
      console.error('Python script error output:', errorOutput);
      return res.status(500).json({ message: 'Error in Python script execution.' });
    }

    if (output === 'Login failed.') {
      return res.status(401).json({ message: 'Login failed. Invalid credentials.' });
    }

    // Check if the user already exists
    const existingUser = await usersCollection.findOne({ rollNo });
    if (existingUser) {
      return res.status(409).json({ message: 'User already registered.' });
    }

    // Insert the new user
    await usersCollection.insertOne({ rollNo, password, notifications: false, cgpa : null, marks : []});
    res.json({ message: 'Registration successful!' });

  } catch (error) {
    console.error('Error during registration:', error);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// Login route
app.post('/login', async (req, res) => {
  const { rollNo, password } = req.body;

  try {
    const user = await usersCollection.findOne({ rollNo, password });

    if (user) {
      res.json(user);  // Return the user object
    } else {
      res.status(401).json({ message: 'Invalid credentials. Please try again.' });
    }

  } catch (error) {
    console.error('Error during login:', error);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// Profile fetching route
app.get('/profile', async (req, res) => {
  const { rollNo } = req.query;

  try {
    const user = await usersCollection.findOne({ rollNo });

    if (user) {
      res.json(user);
    } else {
      res.status(404).json({ message: 'User not found.' });
    }

  } catch (error) {
    console.error('Error fetching profile:', error);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// Update notification preferences
app.post('/notifications', async (req, res) => {
  const { rollNo, notifications } = req.body;

  try {
    const result = await usersCollection.updateOne({ rollNo }, { $set: { notifications } });

    if (result.matchedCount > 0) {
      res.json({ message: 'Notification preference updated successfully!' });
    } else {
      res.status(404).json({ message: 'User not found.' });
    }

  } catch (error) {
    console.error('Error updating notifications:', error);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});
