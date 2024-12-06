import React from 'react';
import { useNavigate } from 'react-router-dom';

const ThankYou = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#453c5e] via-[#b398c0] to-[#7c4d8f] relative overflow-hidden">
      {/* Background text */}
      <div className="absolute inset-0 flex justify-center items-center overflow-hidden">
        <h1 className="text-9xl text-white opacity-10 transform rotate-45 animate-background-text">
          ACPNS
        </h1>
      </div>
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-md text-center relative z-10">
        <h2 className="text-4xl font-extrabold text-gray-800 mb-4">Thank You!</h2>
        <p className="text-lg text-gray-600 mb-6">
          You have successfully registered. You can now log in with your new account.
        </p>
        <button
          onClick={() => navigate('/login')}
          className="relative inline-flex items-center justify-center w-full py-4 px-6 text-lg font-bold text-white bg-[#5b2a6e] rounded-lg shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-[#362e49]/50 border border-[#5b2a6e] group"
        >
          <span className="relative z-10">Go to Login</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#362e49] to-[#5b2a6e] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </div>
    </div>
  );
};

export default ThankYou;
