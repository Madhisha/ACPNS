import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Contact = () => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [alertMessage, setAlertMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('https://notifii-backend-three.vercel.app/send-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        setAlertMessage(result.message);
        // Reset the form
        setFormData({ name: '', email: '', message: '' });
      } else {
        setAlertMessage(`Error: ${result.message}`);
      }
    } catch (error) {
      setAlertMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#453c5e] via-[#b398c0] to-[#7c4d8f] px-4">
      <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-8 text-center" style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)' }}>
        Get in Touch
      </h1>
      <p className="text-xl md:text-2xl text-center text-white mb-12" style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)' }}>
        We’d love to hear from you! Please fill out the form below.
      </p>

      {alertMessage && (
        <div className="mb-4 text-lg text-center text-red-500">
          {alertMessage}
        </div>
      )}

      {/* Contact Form */}
      <form onSubmit={handleSubmit} className="bg-white p-8 md:p-12 rounded-2xl shadow-xl max-w-lg w-full">
        <div className="relative mb-6">
          <label className="block text-[#5b2a6e] mb-2">Name</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="block w-full p-4 border border-[#5b2a6e] rounded-lg text-gray-700 focus:outline-none focus:border-[#BFACC8] focus:ring-2 focus:ring-[#BFACC8] transition duration-200"
            placeholder="Your Name"
            required
          />
        </div>

        <div className="relative mb-6">
          <label className="block text-[#5b2a6e] mb-2">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="block w-full p-4 border border-[#5b2a6e] rounded-lg text-gray-700 focus:outline-none focus:border-[#BFACC8] focus:ring-2 focus:ring-[#BFACC8] transition duration-200"
            placeholder="Your Email"
            required
          />
        </div>

        <div className="relative mb-6">
          <label className="block text-[#5b2a6e] mb-2">Message</label>
          <textarea
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows="4"
            className="block w-full p-4 border border-[#5b2a6e] rounded-lg text-gray-700 focus:outline-none focus:border-[#BFACC8] focus:ring-2 focus:ring-[#BFACC8] transition duration-200"
            placeholder="Your Message"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          className="relative inline-flex items-center justify-center w-full py-4 px-6 text-lg font-bold text-white bg-[#5b2a6e] rounded-lg shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-[#362e49]/50 border border-[#5b2a6e] group"
        >
          <span className="relative z-10">Send Message</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#362e49] to-[#5b2a6e] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </form>
    </div>
  );
};

export default Contact;
