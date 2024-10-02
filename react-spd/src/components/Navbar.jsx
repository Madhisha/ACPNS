import React, { useState } from 'react';
import './styles.css'; // Ensure this path is correct

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-gradient-to-r from-[#C8C6D7] via-[#BFACC8] to-[#E0DFF5] bg-opacity-90 shadow-lg">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/*  Brand */ }
        <div className="text-[#4F1271] text-xl font-bold cookie-regular flex items-center">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="mr-2">
            <path d="M18.5 16C20.433 16 22 13.0899 22 9.5C22 5.91015 20.433 3 18.5 3M18.5 16C16.567 16 15 13.0899 15 9.5C15 5.91015 16.567 3 18.5 3M18.5 16L5.44354 13.6261C4.51605 13.4575 4.05231 13.3731 3.67733 13.189C2.91447 12.8142 2.34636 12.1335 2.11414 11.3159C2 10.914 2 10.4427 2 9.5C2 8.5573 2 8.08595 2.11414 7.68407C2.34636 6.86649 2.91447 6.18577 3.67733 5.81105C4.05231 5.62685 4.51605 5.54254 5.44354 5.3739L18.5 3M5 14L5.39386 19.514C5.43126 20.0376 5.44996 20.2995 5.56387 20.4979C5.66417 20.6726 5.81489 20.8129 5.99629 20.9005C6.20232 21 6.46481 21 6.98979 21H8.7722C9.37234 21 9.67242 21 9.89451 20.8803C10.0897 20.7751 10.2443 20.6081 10.3342 20.4055C10.4365 20.1749 10.4135 19.8757 10.3675 19.2773L10 14.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <a href="/" className="hover:text-[#783F8E] hover:scale-105 transition-all duration-300 ">
            notifii
          </a>
        </div>

        {/* /* Mobile Menu Button  */}
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
