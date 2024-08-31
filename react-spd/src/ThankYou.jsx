import React from 'react';
import { useNavigate } from 'react-router-dom';

const ThankYou = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-purple-600 to-blue-500">
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-md text-center">
        <h2 className="text-4xl font-extrabold text-gray-800 mb-4">Thank You!</h2>
        <p className="text-lg text-gray-600 mb-6">You have successfully registered. You can now log in with your new account.</p>
        <button
          onClick={() => navigate('/')}
          className="py-3 px-6 bg-blue-600 text-white font-bold rounded-full hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:ring-opacity-50 transition duration-300 ease-in-out transform hover:scale-105"
        >
          Go to Login
        </button>
      </div>
    </div>
  );
};

export default ThankYou;
