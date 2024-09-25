import React from 'react';

const Contact = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#4A4063] via-[#BFACC8] to-[#783F8E] px-4 md:px-0">
      <h1 className="text-5xl md:text-7xl font-extrabold text-center text-white mb-8">
        Get in Touch
      </h1>
      <p className="text-xl md:text-2xl text-center text-white mb-12">
        We’d love to hear from you! Please fill out the form below.
      </p>

      {/* Contact Form */}
      <form className="bg-white shadow-lg rounded-lg p-8 max-w-lg w-full">
        <div className="mb-6">
          <label className="block text-[#783F8E] text-sm font-bold mb-2" htmlFor="name">
            Name
          </label>
          <input
            type="text"
            id="name"
            placeholder="Your Name"
            className="border border-[#783F8E] rounded-lg w-full py-2 px-4 focus:outline-none focus:border-[#BFACC8]"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-[#783F8E] text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            type="email"
            id="email"
            placeholder="Your Email"
            className="border border-[#783F8E] rounded-lg w-full py-2 px-4 focus:outline-none focus:border-[#BFACC8]"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-[#783F8E] text-sm font-bold mb-2" htmlFor="message">
            Message
          </label>
          <textarea
            id="message"
            rows="4"
            placeholder="Your Message"
            className="border border-[#783F8E] rounded-lg w-full py-2 px-4 focus:outline-none focus:border-[#BFACC8]"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          className="relative inline-flex items-center justify-center w-full py-4 px-6 text-lg font-bold text-white bg-[#783F8E] rounded-lg shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-[#4A4063]/50 border border-[#783F8E] group"
        >
          <span className="relative z-10">Send Message</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#4A4063] to-[#783F8E] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </form>

      {/* Company Information Section */}
      <div className="mt-12 text-center">
        <h2 className="text-3xl font-bold text-white mb-4">Our Office</h2>
        <p className="text-lg text-white">12345 Example Road</p>
        <p className="text-lg text-white">City, State, 12345</p>
        <p className="text-lg text-white">Email: contact@example.com</p>
        <p className="text-lg text-white">Phone: (123) 456-7890</p>
      </div>
    </div>
  );
};

export default Contact;
