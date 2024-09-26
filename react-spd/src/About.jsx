import React from 'react';

const AboutUs = () => {
  return (
    <div className="text-gray-800">
      {/* Hero Section */}
      <div className="relative w-full h-72 bg-cover bg-center" style={{ backgroundImage: 'url(https://source.unsplash.com/random/1920x1080)' }}>
        <div className="relative flex flex-col items-center justify-center h-full">
          <p className="text-4xl md:text-6xl font-bold text-[#5b2a6e] text-center">About Us</p>
          <p className="mt-4 text-center max-w-xl"> 
            ACPNS is a platform for students to get all the information about their college at one place without missing any updates from the college portal.
          </p>
        </div>

      </div>

      {/* Team Section */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-8 text-[#5b2a6e]">Meet Our Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Team Member Card 1 */}
          <div className="bg-[#e6d7e8] rounded-lg p-6 text-center shadow-lg">
            <img src="\src\assets\profile.jpg" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-[#5b2a6e]">Jeevashakthi V</h3>
            {/* <p className="text-gray-600"></p>
            <p className="mt-2">
              John is passionate about travel and innovation, leading our team with a vision for the future.
            </p> */}
          </div>
          {/* Team Member Card 2 */}
          <div className="bg-[#e6d7e8] rounded-lg p-6 text-center shadow-lg">
            <img src="\src\assets\profile.jpg" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-[#5b2a6e]">Aravinth Cheran K S</h3>
            {/* <p className="text-gray-600"></p>
            <p className="mt-2">
              Jane drives the technological advancements that keep our services ahead of the competition.
            </p> */}
          </div>
          {/* Team Member Card 3 */}
          <div className="bg-[#e6d7e8] rounded-lg p-6 text-center shadow-lg">
            <img src="\src\assets\profile.jpg" alt="Team Member" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-[#5b2a6e]">Madhisha S</h3>
            {/* <p className="text-gray-600"></p>
            <p className="mt-2">
              Alice is responsible for our outreach efforts, making sure everyone knows about our amazing services.
            </p> */}
            
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutUs;
