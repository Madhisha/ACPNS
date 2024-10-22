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
        <div className="text-[#4F1271] text-xl font-bold the-nautigal-bold flex items-center">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#783F8E" stroke-width="1.224" className="mr-2">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.7942 3.29494C13.2296 3.10345 12.6258 3 12 3C9.15347 3 6.76217 5.14032 6.44782 7.96942L6.19602 10.2356L6.18957 10.2933C6.06062 11.417 5.69486 12.5005 5.11643 13.4725L5.08664 13.5222L4.5086 14.4856C3.98405 15.3599 3.72177 15.797 3.77839 16.1559C3.81607 16.3946 3.93896 16.6117 4.12432 16.7668C4.40289 17 4.91267 17 5.93221 17H18.0678C19.0873 17 19.5971 17 19.8756 16.7668C20.061 16.6117 20.1839 16.3946 20.2216 16.1559C20.2782 15.797 20.0159 15.3599 19.4914 14.4856L18.9133 13.5222L18.8835 13.4725C18.4273 12.7059 18.1034 11.8698 17.9236 10.9994C15.1974 10.9586 13 8.73592 13 6C13 5.00331 13.2916 4.07473 13.7942 3.29494ZM16.2741 4.98883C16.0999 5.28551 16 5.63109 16 6C16 6.94979 16.662 7.74494 17.5498 7.94914C17.4204 6.82135 16.9608 5.80382 16.2741 4.98883Z" fill="#783F8E"></path>
            <path d="M9 17C9 17.394 9.0776 17.7841 9.22836 18.1481C9.37913 18.512 9.6001 18.8427 9.87868 19.1213C10.1573 19.3999 10.488 19.6209 10.8519 19.7716C11.2159 19.9224 11.606 20 12 20C12.394 20 12.7841 19.9224 13.1481 19.7716C13.512 19.6209 13.8427 19.3999 14.1213 19.1213C14.3999 18.8427 14.6209 18.512 14.7716 18.1481C14.9224 17.7841 15 17.394 15 17L12 17H9Z" fill="#783F8E"></path>
            <circle cx="18" cy="6" r="2.5" fill="#783F8E" stroke="#783F8E"></circle>
          </svg>
          <a href="/" className="hover:text-[#783F8E] hover:scale-105 transition-all duration-300">
            Notifii
          </a>
        </div>


        {/* Mobile Menu Button  */}
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
          {/* <li>
            <a
              href="/register"
              className="relative hover:text-[#783F8E] hover:scale-105 transition-all duration-300 before:content-[''] before:absolute before:left-0 before:bottom-[-2px] before:w-0 before:h-0.5 before:bg-[#783F8E] before:transition-all before:duration-300 hover:before:w-full"
            >
              Register
            </a>
          </li> */}
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
