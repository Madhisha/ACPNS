import React, { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 shadow-lg">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/* Brand */}
        <div className="text-white text-2xl font-bold">
          <a href="/" className="hover:text-gray-200 transition-colors duration-300">
            ACPNS
          </a>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <button
            onClick={toggleMenu}
            className="text-white focus:outline-none transition-transform transform duration-300 ease-in-out"
          >
            {isOpen ? (
              <svg
                className="w-6 h-6 animate-spin"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            ) : (
              <svg
                className="w-6 h-6 transition-transform transform duration-300 ease-in-out"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16"
                ></path>
              </svg>
            )}
          </button>
        </div>

        {/* Links for desktop */}
        <ul className="hidden md:flex space-x-6 text-white font-semibold">
          <li>
            <a href="/" className="hover:text-gray-200 transition-colors duration-300">Home</a>
          </li>
          <li>
            <a href="/about" className="hover:text-gray-200 transition-colors duration-300">About</a>
          </li>
          <li>
            <a href="/contact" className="hover:text-gray-200 transition-colors duration-300">Contact</a>
          </li>
          <li>
            <a href="/register" className="hover:text-gray-200 transition-colors duration-300">Register</a>
          </li>
          <li>
            <a href="/login" className="hover:text-gray-200 transition-colors duration-300">Login</a>
          </li>
        </ul>
      </div>

      {/* Mobile Menu with smooth slide down */}
      <div
        className={`md:hidden overflow-hidden transition-all duration-500 ease-in-out transform ${
          isOpen ? 'max-h-80 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <ul className="flex flex-col space-y-2 px-6 py-4 text-white font-semibold">
          <li>
            <a href="/" className="hover:text-gray-200 transition-colors duration-300">Home</a>
          </li>
          <li>
            <a href="/about" className="hover:text-gray-200 transition-colors duration-300">About</a>
          </li>
          <li>
            <a href="/contact" className="hover:text-gray-200 transition-colors duration-300">Contact</a>
          </li>
          <li>
            <a href="/register" className="hover:text-gray-200 transition-colors duration-300">Register</a>
          </li>
          <li>
            <a href="/login" className="hover:text-gray-200 transition-colors duration-300">Login</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
