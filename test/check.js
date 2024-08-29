const { spawnSync } = require('child_process');

const user = '22z212'
const password = 'cheran#212'


// Run the Python script
const pythonProcess = spawnSync('python', ['login.py', user, password]);

if (pythonProcess.error) {
    console.error('Error executing Python script:', pythonProcess.error);
}

const output = pythonProcess.stdout.toString().trim();
const errorOutput = pythonProcess.stderr.toString().trim()

if (errorOutput) {
    console.error('Python script error output:', errorOutput);
}

if (output.toLowerCase().includes('login failed')) {
    console.log('Login failed. Invalid credentials.')
}
else {
    console.log('Registration successful!')
}