import React from 'react';

const AboutUs = () => {
  return (
    <div className="bg-white text-gray-800">
      {/* Hero Section */}
      <div className="relative w-full h-72 bg-cover bg-center" style={{ backgroundImage: 'url(https://source.unsplash.com/random/1920x1080)' }}>
        <div className="absolute inset-0 bg-black opacity-50"></div>
        <div className="relative flex items-center justify-center h-full">
          <h1 className="text-4xl md:text-6xl font-bold text-white text-center">About Us</h1>
        </div>
      </div>

      {/* Mission Statement Section */}
      <div className="max-w-7xl mx-auto px-6 py-12 text-center">
        <h2 className="text-3xl md:text-5xl font-bold mb-4 text-blue-600">Our Mission</h2>
        <p className="text-lg md:text-xl mb-6">
          To provide seamless and innovative travel solutions that empower people to explore the world effortlessly.
        </p>
      </div>

      {/* Team Section */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-8 text-blue-600">Meet Our Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Team Member Card 1 */}
          <div className="bg-blue-50 rounded-lg p-6 text-center shadow-md">
            <img src="https://source.unsplash.com/random/200x200?person" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-blue-600">John Doe</h3>
            <p className="text-gray-600">CEO & Founder</p>
            <p className="mt-2">
              John is passionate about travel and innovation, leading our team with a vision for the future.
            </p>
          </div>
          {/* Team Member Card 2 */}
          <div className="bg-blue-50 rounded-lg p-6 text-center shadow-md">
            <img src="https://source.unsplash.com/random/200x200?person" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-blue-600">Jane Smith</h3>
            <p className="text-gray-600">Chief Technology Officer</p>
            <p className="mt-2">
              Jane drives the technological advancements that keep our services ahead of the competition.
            </p>
          </div>
          {/* Team Member Card 3 */}
          <div className="bg-blue-50 rounded-lg p-6 text-center shadow-md">
            <img src="https://source.unsplash.com/random/200x200?person" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-blue-600">Alice Johnson</h3>
            <p className="text-gray-600">Marketing Director</p>
            <p className="mt-2">
              Alice is responsible for our outreach efforts, making sure everyone knows about our amazing services.
            </p>
          </div>
        </div>
      </div>

      {/* Values Section */}
      <div className="bg-blue-50 py-12">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl md:text-5xl font-bold text-center mb-8 text-blue-600">Our Values</h2>
          <ul className="list-disc list-inside text-lg md:text-xl">
            <li>Integrity: We operate with honesty and transparency.</li>
            <li>Innovation: We embrace change and seek out new solutions.</li>
            <li>Customer Focus: We prioritize our customers' needs and experiences.</li>
            <li>Teamwork: We collaborate to achieve common goals.</li>
          </ul>
        </div>
      </div>

      {/* Contact Section */}
      <div className="max-w-7xl mx-auto px-6 py-12 text-center">
        <h2 className="text-3xl md:text-5xl font-bold mb-4 text-blue-600">Get in Touch</h2>
        <p className="text-lg md:text-xl mb-6">
          We would love to hear from you! Reach out to us for any inquiries.
        </p>
        <button className="bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700 transition duration-300">
          Contact Us
        </button>
      </div>
    </div>
  );
};

export default AboutUs;
