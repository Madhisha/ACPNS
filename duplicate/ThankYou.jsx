import React from 'react';
import { useNavigate } from 'react-router-dom';

const ThankYou = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl font-semibold mb-6">Thank You for Registering!</h2>
      <p className="mb-6">You can now log in with your new account.</p>
      <button
        onClick={() => navigate('/')}
        className="py-2 px-4 bg-blue-500 text-white font-bold rounded hover:bg-blue-600 transition duration-200"
      >
        Go to Login
      </button>
    </div>
  );
};

export default ThankYou;
