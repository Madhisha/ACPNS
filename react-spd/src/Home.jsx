import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-600 to-green-500 px-4 md:px-0">
      <h1 className="text-4xl md:text-6xl font-bold text-white mb-8 text-center">
        Welcome to Our College Portal
      </h1>
      <p className="text-lg md:text-2xl text-white text-center mb-8">
        Access your attendance, timetable, seating arrangement, and CGPA details all in one place.
      </p>
      
      {/* Animated buttons for Login and Register */}
      <div className="w-full max-w-sm space-y-4">
        <button
          className="group/button w-full relative inline-flex items-center justify-center overflow-hidden rounded-md bg-gray-900/30 backdrop-blur-lg px-6 py-4 text-base font-semibold text-white transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-xl hover:shadow-gray-600/50 border border-white/20"
          onClick={() => navigate('/login')}
        >
          <span className="text-lg">Login</span>
          <div className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-13deg)_translateX(-100%)] group-hover/button:duration-1000 group-hover/button:[transform:skew(-13deg)_translateX(100%)]">
            <div className="relative h-full w-10 bg-gray-800/20"></div>
          </div>
        </button>

        <button
          className="group/button w-full relative inline-flex items-center justify-center overflow-hidden rounded-md bg-gray-800/30 backdrop-blur-lg px-6 py-4 text-base font-semibold text-white transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-xl hover:shadow-gray-600/50 border border-white/20"
          onClick={() => navigate('/register')}
        >
          <span className="text-lg">Register</span>
          <div className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-13deg)_translateX(-100%)] group-hover/button:duration-1000 group-hover/button:[transform:skew(-13deg)_translateX(100%)]">
            <div className="relative h-full w-10 bg-gray-700/20"></div>
          </div>
        </button>
      </div>
    </div>
  );
};

export default Home;
