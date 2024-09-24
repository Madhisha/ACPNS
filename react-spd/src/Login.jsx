import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [rollNo, setRollNo] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rollNo, password }),
      });

      if (response.status === 200) {
        const userData = await response.json();  // Get user data from response
        navigate('/welcome', { state: userData });  // Navigate and pass user data as state
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error during login:', error);
      setError('Error: Could not connect to the server. Please try again later.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-400 to-purple-600">
      <h2 className="text-3xl font-bold text-white mb-6">Login Page</h2>
      <form onSubmit={handleLogin} className="bg-white p-10 rounded-2xl shadow-lg max-w-md w-full">
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
            required
          />
        </div>

        {/* Login Button */}
        <button
          type="submit"
          className="group/button w-full relative inline-flex items-center justify-center overflow-hidden rounded-md bg-blue-600 backdrop-blur-lg px-6 py-3 text-base font-semibold text-white transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-xl hover:shadow-blue-700/50 border border-blue-800"
        >
          <span className="text-lg">Login</span>
          <div
            className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-13deg)_translateX(-100%)] group-hover/button:duration-1000 group-hover/button:[transform:skew(-13deg)_translateX(100%)]"
          >
            <div className="relative h-full w-10 bg-blue-700/30"></div>
          </div>
        </button>

        {/* Register Button */}
        <button
          type="button"
          onClick={() => navigate('/register')}
          className="group/button w-full relative inline-flex items-center justify-center overflow-hidden rounded-md bg-green-600 backdrop-blur-lg px-6 py-3 text-base font-semibold text-white transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-xl hover:shadow-green-700/50 border border-green-800 mt-4"
        >
          <span className="text-lg">Register</span>
          <div
            className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-13deg)_translateX(-100%)] group-hover/button:duration-1000 group-hover/button:[transform:skew(-13deg)_translateX(100%)]"
          >
            <div className="relative h-full w-10 bg-green-700/30"></div>
          </div>
        </button>
      </form>
    </div>
  );
};

export default Login;
