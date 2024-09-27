const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawnSync } = require('child_process');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const PORT = 3000;
const USERS_FILE = 'registered_users.json';

// Initialize the server and ensure the users file exists
app.listen(PORT, () => {
  console.log(`Server running on http://127.0.0.1:${PORT}`);
  if (!fs.existsSync(USERS_FILE)) {
    fs.writeFileSync(USERS_FILE, JSON.stringify([])); // Initialize as an empty array
  }
});

// Register route
app.post('/register', (req, res) => {
  const { rollNo, password } = req.body;

  try {
    // Run the Python script
    const pythonProcess = spawnSync('python', ['login.py', rollNo, password]);

    if (pythonProcess.error) {
      console.error('Error executing Python script:', pythonProcess.error);
      return res.status(500).json({ message: 'Error executing Python script.' });
    }

    const output = pythonProcess.stdout.toString().trim();
    console.log('Python script output:', output);
    const errorOutput = pythonProcess.stderr.toString().trim();

    if (errorOutput) {
      console.error('Python script error output:', errorOutput);
      return res.status(500).json({ message: 'Error in Python script execution.' });
    }

    if (output === 'Login failed.') {
      console.log('Login failed. Invalid credentials.');
      return res.status(401).json({ message: 'Login failed. Invalid credentials.' });
    }

    // Read existing users
    let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));

    // Append the new user
    users.push({ rollNo, password, notifications: false });
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));

    res.json({ message: 'Registration successful!' });

  } catch (error) {
    console.error('Error during registration:', error);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// Login route
app.post('/login', (req, res) => {
  console.log('Login endpoint hit');
  const { rollNo, password } = req.body;
  console.log('Received credentials:', { rollNo, password });

  try {
    // Read existing users
    let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));
    console.log('Registered users:', users);

    const user = users.find(user => user.rollNo === rollNo && user.password === password);

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
app.get('/profile', (req, res) => {
  const { rollNo } = req.query;

  try {
    let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));
    const user = users.find(user => user.rollNo === rollNo);

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
app.post('/notifications', (req, res) => {
  const { rollNo, notifications } = req.body;

  try {
    // Read existing users
    let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));
    const userIndex = users.findIndex(user => user.rollNo === rollNo);

    if (userIndex !== -1) {
      users[userIndex].receive_notifications = notifications;
      fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
      res.json({ message: 'Notification preference updated successfully!' });
    } else {
      res.status(404).json({ message: 'User not found.' });
    }

  } catch (error) {
    console.error('Error updating notifications:', error);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});
