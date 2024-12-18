import React from 'react';
import { useNavigate } from 'react-router-dom';
import "../src/index.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#453c5e] via-[#b398c0] to-[#7c4d8f] px-4 md:px-0">
      <h1 
        className="text-5xl md:text-7xl font-extrabold text-white mb-6 text-center"
        style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)' }} // Add letter shadow here
      >
        Connect. Learn. Thrive.
      </h1>
      <p 
        className="text-xl md:text-3xl text-white text-center mb-8"
        style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.7)' }} // Add letter shadow here
      >
        Get notified from your portal for attendance, timetable, seating arrangements, and CGPA details.
      </p>
      {/* Animated Buttons for Login and Register */}
      <div className="w-full max-w-md space-y-6">
        <button
          className="relative inline-flex items-center justify-center w-full px-6 py-4 text-lg font-bold text-white bg-[#5b2a6e] rounded-lg overflow-hidden shadow-lg transform transition-all duration-300 group hover:scale-105 hover:shadow-lg hover:shadow-[#362e49]/50"
          onClick={() => navigate('/login')}
        >
          <span className="z-10 relative">Login Now</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#362e49] to-[#5b2a6e] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>

        <button
          className="relative inline-flex items-center justify-center w-full px-6 py-4 text-lg font-bold text-white bg-[#362e49] rounded-lg overflow-hidden shadow-lg transform transition-all duration-300 group hover:scale-105 hover:shadow-lg hover:shadow-[#362e49]/50"
          onClick={() => navigate('/register')}
        >
          <span className="z-10 relative">Register Today</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#362e49] to-[#5b2a6e] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </div>

      {/* Notification Phrases */}
      <div className="mt-12 text-white text-center">
        <h2 
          className="text-2xl md:text-4xl font-semibold" 
          style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.7)' }} // Add letter shadow here
        >
          Stay Updated
        </h2>
        <p 
          className="mt-2 text-lg md:text-xl" 
          style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.7)' }} // Add letter shadow here
        >
          "Don't miss out on important notifications. Register today!"
        </p>
      </div>
    </div>
  );
};

export default Home;
