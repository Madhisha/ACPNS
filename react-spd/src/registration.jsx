import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Registration = () => {
  const [rollNo, setRollNo] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-purple-600 via-pink-500 to-indigo-500 px-4">
      <h2 className="text-5xl md:text-7xl font-extrabold text-white mb-8 text-center">
        Join the Community
      </h2>
      <form onSubmit={handleSubmit} className="bg-white p-8 md:p-12 rounded-2xl shadow-xl max-w-lg w-full">
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <div className="relative mb-6">
          <input
            type="text"
            value={rollNo}
            onChange={(e) => setRollNo(e.target.value)}
            className="block w-full p-4 pt-6 border border-blue-400 rounded-lg text-gray-700 placeholder-transparent focus:outline-none transition duration-200 peer"
            placeholder="Write here..."
            required
          />
          <label
            className="absolute top-0 left-3 px-1 text-blue-500 bg-white transform -translate-y-2.5 scale-90 peer-placeholder-shown:translate-y-3 peer-placeholder-shown:scale-100 peer-placeholder-shown:text-gray-400 transition-all duration-200"
          >
            Roll No
          </label>
        </div>
        <div className="relative mb-6">
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="block w-full p-4 pt-6 border border-blue-400 rounded-lg text-gray-700 placeholder-transparent focus:outline-none transition duration-200 peer"
            placeholder="Write here..."
            required
          />
          <label
            className="absolute top-0 left-3 px-1 text-blue-500 bg-white transform -translate-y-2.5 scale-90 peer-placeholder-shown:translate-y-3 peer-placeholder-shown:scale-100 peer-placeholder-shown:text-gray-400 transition-all duration-200"
          >
            Password
          </label>
          {/* Eye Icon */}
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-4 flex items-center text-gray-500"
          >
            {/* Font Awesome Icon */}
            <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'} text-xl`}></i>
          </button>
        </div>
        <button
          type="submit"
          className="relative inline-flex items-center justify-center w-full py-4 px-6 text-lg font-bold text-white bg-purple-600 rounded-lg shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-purple-700/50 border border-purple-700 group"
        >
          <span className="relative z-10">Register</span>
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </form>
    </div>
  );
};

export default Registration;
