import React from 'react';

const AboutUs = () => {
  return (
    <div className="text-gray-800">
      {/* Hero Section */}
      <div className="relative w-full h-72 bg-cover bg-center" style={{ backgroundImage: 'url(https://source.unsplash.com/random/1920x1080)' }}>
        <div className="relative flex flex-col items-center justify-center h-full text-center">
          <p className="text-4xl md:text-6xl font-bold text-[#5b2a6e]">About Us</p>
          <p className="mt-4 max-w-2xl mx-auto text-lg md:text-xl"> 
            ACPNS is a platform that helps students access all their essential college information in one place. From academic schedules to important updates, ACPNS ensures students stay informed without missing anything from the college portal. With real-time notifications, students can easily keep track of their academic journey.
          </p>
        </div>
      </div>

      {/* Team Section */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-8 text-[#5b2a6e]">Meet Our Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Team Member Card 1 */}
          <div className="bg-[#e6d7e8] rounded-lg p-6 text-center shadow-lg">
            <img src="profile.jpg" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-[#5b2a6e]">Jeevashakthi V</h3>
          </div>
          {/* Team Member Card 2 */}
          <div className="bg-[#e6d7e8] rounded-lg p-6 text-center shadow-lg">
            <img src="profile.jpg" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-[#5b2a6e]">Aravinth Cheran K S</h3>
          </div>
          {/* Team Member Card 3 */}
          <div className="bg-[#e6d7e8] rounded-lg p-6 text-center shadow-lg">
            <img src="profile.jpg" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-[#5b2a6e]">Madhisha S</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutUs;
