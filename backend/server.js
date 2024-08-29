const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawnSync } = require('child_process');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());
app.use(cors());



const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

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

        // Save to text file upon successful login
        fs.appendFileSync('registered_users.txt', `${rollNo}:${password}\n`);
        res.json({ message: 'Registration successful!' });

    } catch (error) {
        console.error('Error during registration:', error);
        res.status(500).json({ message: 'Server error. Please try again later.' });
    }
});