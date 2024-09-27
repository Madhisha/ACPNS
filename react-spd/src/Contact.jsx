import React, { useState } from 'react';

const Contact = () => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [alertMessage, setAlertMessage] = useState('');

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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#4A4063] via-[#BFACC8] to-[#783F8E] px-4 md:px-0">
      <h1 className="text-5xl md:text-7xl font-extrabold text-center text-white mb-8">Get in Touch</h1>
      <p className="text-xl md:text-2xl text-center text-white mb-12">We’d love to hear from you! Please fill out the form below.</p>

      {alertMessage && (
        <div className="mb-4 text-lg text-center text-white">{alertMessage}</div>
      )}

      {/* Contact Form */}
      <form className="bg-white shadow-lg rounded-lg p-8 max-w-lg w-full" onSubmit={handleSubmit}>
        <div className="mb-6">
          <label className="block text-[#783F8E] text-sm font-bold mb-2" htmlFor="name">Name</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Your Name"
            className="border border-[#BFACC8] rounded-lg w-full py-2 px-4 focus:outline-none focus:border-[#5b2a6e]"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-[#783F8E] text-sm font-bold mb-2" htmlFor="email">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Your Email"
            className="border border-[#BFACC8] rounded-lg w-full py-2 px-4 focus:outline-none focus:border-[#5b2a6e]"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-[#783F8E] text-sm font-bold mb-2" htmlFor="message">Message</label>
          <textarea
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows="4"
            placeholder="Your Message"
            className="border border-[#BFACC8] rounded-lg w-full py-2 px-4 focus:outline-none focus:border-[#5b2a6e]"
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