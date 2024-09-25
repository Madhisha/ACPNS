import React, { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-gradient-to-r from-[#C8C6D7] via-[#BFACC8] to-[#E0DFF5] bg-opacity-90 shadow-lg">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/* Brand */}
        <div className="text-[#4F1271] text-2xl font-bold">
          <a href="/" className="hover:text-[#783F8E] hover:scale-105 transition-all duration-300">
            ACPNS
          </a>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <button
            onClick={toggleMenu}
            className="text-[#4F1271] focus:outline-none transition-transform transform duration-300 ease-in-out"
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
        <ul className="hidden md:flex space-x-6 text-[#4F1271] font-semibold">
          <li>
            <a
              href="/"
              className="relative hover:text-[#783F8E] hover:scale-105 transition-all duration-300 before:content-[''] before:absolute before:left-0 before:bottom-[-2px] before:w-0 before:h-0.5 before:bg-[#783F8E] before:transition-all before:duration-300 hover:before:w-full"
            >
              Home
            </a>
          </li>
          <li>
            <a
              href="/about"
              className="relative hover:text-[#783F8E] hover:scale-105 transition-all duration-300 before:content-[''] before:absolute before:left-0 before:bottom-[-2px] before:w-0 before:h-0.5 before:bg-[#783F8E] before:transition-all before:duration-300 hover:before:w-full"
            >
              About
            </a>
          </li>
          <li>
            <a
              href="/contact"
              className="relative hover:text-[#783F8E] hover:scale-105 transition-all duration-300 before:content-[''] before:absolute before:left-0 before:bottom-[-2px] before:w-0 before:h-0.5 before:bg-[#783F8E] before:transition-all before:duration-300 hover:before:w-full"
            >
              Contact
            </a>
          </li>
          <li>
            <a
              href="/register"
              className="relative hover:text-[#783F8E] hover:scale-105 transition-all duration-300 before:content-[''] before:absolute before:left-0 before:bottom-[-2px] before:w-0 before:h-0.5 before:bg-[#783F8E] before:transition-all before:duration-300 hover:before:w-full"
            >
              Register
            </a>
          </li>
          <li>
            <a
              href="/login"
              className="relative hover:text-[#783F8E] hover:scale-105 transition-all duration-300 before:content-[''] before:absolute before:left-0 before:bottom-[-2px] before:w-0 before:h-0.5 before:bg-[#783F8E] before:transition-all before:duration-300 hover:before:w-full"
            >
              Login
            </a>
          </li>
        </ul>
      </div>

      {/* Mobile Menu with smooth slide down */}
      <div
        className={`md:hidden overflow-hidden transition-all duration-500 ease-in-out transform ${
          isOpen ? 'max-h-80 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <ul className="flex flex-col space-y-2 px-6 py-4 text-[#4F1271] font-semibold">
          <li>
            <a href="/" className="hover:text-[#783F8E] transition-colors duration-300">Home</a>
          </li>
          <li>
            <a href="/about" className="hover:text-[#783F8E] transition-colors duration-300">About</a>
          </li>
          <li>
            <a href="/contact" className="hover:text-[#783F8E] transition-colors duration-300">Contact</a>
          </li>
          <li>
            <a href="/register" className="hover:text-[#783F8E] transition-colors duration-300">Register</a>
          </li>
          <li>
            <a href="/login" className="hover:text-[#783F8E] transition-colors duration-300">Login</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
