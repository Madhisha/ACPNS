import React from 'react';
import { Link } from 'react-router-dom';

const ThankYou = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-3xl font-semibold mb-6">Thank You for Registering!</h2>
      <p className="mb-6">Your registration has been successfully completed.</p>
      <Link to="/">
        <button className="py-2 px-4 bg-blue-500 text-white font-bold rounded hover:bg-blue-600 transition duration-200">
          Go to Home
        </button>
      </Link>
    </div>
  );
};

export default ThankYou;
