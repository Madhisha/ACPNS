import React from 'react';

const Contact = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4 md:px-0">
      <h1 className="text-5xl md:text-7xl font-extrabold text-center text-purple-600 mb-8">
        Get in Touch
      </h1>
      <p className="text-xl md:text-2xl text-center mb-12">
        We’d love to hear from you! Please fill out the form below.
      </p>

      {/* Contact Form */}
      <form className="bg-white shadow-lg rounded-lg p-8 max-w-lg w-full">
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
            Name
          </label>
          <input
            type="text"
            id="name"
            placeholder="Your Name"
            className="border border-gray-300 rounded-lg w-full py-2 px-4 focus:outline-none focus:border-purple-500"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            type="email"
            id="email"
            placeholder="Your Email"
            className="border border-gray-300 rounded-lg w-full py-2 px-4 focus:outline-none focus:border-purple-500"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="message">
            Message
          </label>
          <textarea
            id="message"
            rows="4"
            placeholder="Your Message"
            className="border border-gray-300 rounded-lg w-full py-2 px-4 focus:outline-none focus:border-purple-500"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          className="bg-purple-600 text-white py-3 px-6 rounded-lg shadow-md hover:bg-purple-700 transition duration-300"
        >
          Send Message
        </button>
      </form>

      {/* Company Information Section */}
      <div className="mt-12 text-center">
        <h2 className="text-3xl font-bold text-purple-600 mb-4">Our Office</h2>
        <p className="text-lg text-gray-700">12345 Example Road</p>
        <p className="text-lg text-gray-700">City, State, 12345</p>
        <p className="text-lg text-gray-700">Email: contact@example.com</p>
        <p className="text-lg text-gray-700">Phone: (123) 456-7890</p>
      </div>
    </div>
  );
};

export default Contact;
