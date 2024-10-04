import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Registration = () => {
  const [rollNo, setRollNo] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const [loading,setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      const response = await fetch('https://notifii-backend-three.vercel.app/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rollNo, password }),
      });

      if (response.status === 200) {
        setLoading(false);
        setTimeout(() => navigate('/thank-you'),3000)
        // navigate('/thank-you');

      } else if (response.status === 401) {
        setLoading(false)
        setError('Invalid credentials. Please check your username and password.');
      } else {
        const errorData = await response.json();
        setError(
          errorData.message || 'Registration failed. Please check your credentials and try again.'
        );
        setLoading(false)
      }
    } catch (error) {
      setError('Error: Could not connect to the server. Please try again later.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#453c5e] via-[#b398c0] to-[#7c4d8f] px-4">
      {loading && (
  <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
    <div className="animate-spin-slow w-12 h-12 border-4 border-white border-t-theme-blue-violet rounded-full"></div>
  </div>
)}
      <h2
        className="text-5xl md:text-7xl font-extrabold text-white mb-8 text-center"
        style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)' }}
      >
        Join the Community
      </h2>
      <form onSubmit={handleSubmit} className="bg-white p-8 md:p-12 rounded-2xl shadow-xl max-w-lg w-full">
        {error && (
          <p
            className="text-red-500 mb-4"
            style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
          >
            {error}
          </p>
        )}

        {/* Roll No Field */}
        <div className="relative mb-6">
          <input
            type="text"
            value={rollNo}
            onChange={(e) => setRollNo(e.target.value)}
            className="block w-full p-4 pt-6 border border-[#5b2a6e] rounded-lg text-gray-700 focus:outline-none focus:border-[#BFACC8] focus:ring-2 focus:ring-[#BFACC8] transition duration-200"
            // placeholder="Enter your roll no"
            required
          />
          {/* Fixed Label */}
          <label
            className="absolute top-0 left-3 px-1 text-[#5b2a6e] bg-white transform -translate-y-2.5 scale-90"
          >
            Roll No
          </label>
        </div>

        {/* Password Field */}
        <div className="relative mb-6">
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="block w-full p-4 pt-6 pr-12 border border-[#5b2a6e] rounded-lg text-gray-700 focus:outline-none focus:border-[#BFACC8] focus:ring-2 focus:ring-[#BFACC8] transition duration-200"
            // placeholder="Enter your password"
            required
          />
          {/* Fixed Label */}
          <label
            className="absolute top-0 left-3 px-1 text-[#5b2a6e] bg-white transform -translate-y-2.5 scale-90"
          >
            Password
          </label>

          {/* Eye Icon for showing/hiding password */}
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-4 flex items-center text-gray-500"
          >
            <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'} text-xl`}></i>
          </button>
        </div>

        {/* Register Button */}
        <button
          type="submit"
          className="relative inline-flex items-center justify-center w-full py-4 px-6 text-lg font-bold text-white bg-[#5b2a6e] rounded-lg shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-[#362e49]/50 border border-[#5b2a6e] group"
        >
          <span className="relative z-10">Register</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#362e49] to-[#5b2a6e] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </form>
    </div>
  );
};

export default Registration;
