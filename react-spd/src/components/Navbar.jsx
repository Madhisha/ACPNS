// Navbar.js
import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 shadow-lg">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <div className="text-white text-2xl font-bold">
          <a href="/" className="hover:text-gray-200 transition duration-300">
            ACPNS
          </a>
        </div>
        <ul className="flex space-x-6 text-white font-semibold">
          <li>
            <a href="/" className="hover:text-gray-200 transition duration-300">Home</a>
          </li>
          <li>
            <a href="/about" className="hover:text-gray-200 transition duration-300">About</a>
          </li>
          <li>
            <a href="/contact" className="hover:text-gray-200 transition duration-300">Contact</a>
          </li>
          <li>
            <a href="/register" className="hover:text-gray-200 transition duration-300">Register</a>
          </li>
          <li>
            <a href="/login" className="hover:text-gray-200 transition duration-300">Login</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
