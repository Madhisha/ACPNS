import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Registration = () => {
  const [rollNo, setRollNo] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rollNo, password }),
      });

      if (response.status === 200) {
        navigate('/thank-you');
      } else if (response.status === 401) {
        setError('Invalid credentials. Please check your username and password.');
      } else {
        const errorData = await response.json();
        setError(
          errorData.message || 'Registration failed. Please check your credentials and try again.'
        );
      }
    } catch (error) {
      setError('Error: Could not connect to the server. Please try again later.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-green-400 to-blue-500">
      <h2 className="text-3xl font-bold text-white mb-6">Registration Page</h2>
      <form onSubmit={handleSubmit} className="bg-white p-10 rounded-2xl shadow-lg max-w-md w-full">
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <div className="mb-6">
          <label className="block text-gray-700 font-semibold mb-2">Roll No:</label>
          <input
            type="text"
            value={rollNo}
            onChange={(e) => setRollNo(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 font-semibold mb-2">Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
            title="Enter eCampus password"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full py-3 px-6 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition duration-300"
        >
          Register
        </button>
      </form>
    </div>
  );
};

export default Registration;
