import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Welcome = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(location.state || { rollNo: '', notifications: {}, error: '' });
  const [mainNotificationsEnabled, setMainNotificationsEnabled] = useState(true);

  useEffect(() => {
    if (!location.state) {
      const fetchProfile = async () => {
        try {
          const response = await fetch(`https://notifii-backend-three.vercel.app/profile?rollNo=${profile.rollNo}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (response.status === 200) {
            const data = await response.json();
            setProfile(data);
            setMainNotificationsEnabled(data.notifications.main || true);
          } else {
            setProfile((prev) => ({ ...prev, error: 'Failed to load profile. Please try again later.' }));
          }
        } catch (error) {
          setProfile((prev) => ({ ...prev, error: 'Error: Could not connect to the server. Please try again later.' }));
          console.error('Error fetching profile:', error);
        }
      };

      fetchProfile();
    }
  }, [location.state, profile.rollNo]);

  const handleToggleNotification = async (type) => {
    try {
      const updatedPreference = { ...profile.notifications, [type]: !profile.notifications[type] };
      const response = await fetch('https://notifii-backend-three.vercel.app/notifications', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rollNo: profile.rollNo, notifications: updatedPreference }),
      });

      if (response.status === 200) {
        setProfile((prevProfile) => ({
          ...prevProfile,
          notifications: updatedPreference,
        }));
      } else {
        setProfile((prev) => ({ ...prev, error: 'Failed to update notification preference.' }));
      }
    } catch (error) {
      setProfile((prev) => ({ ...prev, error: 'Error: Could not connect to the server. Please try again later.' }));
      console.error('Error updating notification preference:', error);
    }
  };

  const handleMainToggle = async () => {
    const updatedPreference = !mainNotificationsEnabled;
    setMainNotificationsEnabled(updatedPreference);

    const updatedNotifications = {
      attendance: updatedPreference,
      marks: updatedPreference,
      timetable: updatedPreference,
      seatingArrangement: updatedPreference,
      results: updatedPreference,
    };

    try {
      const response = await fetch('https://notifii-backend-three.vercel.app/notifications', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rollNo: profile.rollNo, notifications: updatedNotifications }),
      });

      if (response.status === 200) {
        setProfile((prevProfile) => ({
          ...prevProfile,
          notifications: updatedNotifications,
        }));
      } else {
        setProfile((prev) => ({ ...prev, error: 'Failed to update notification preference.' }));
      }
    } catch (error) {
      setProfile((prev) => ({ ...prev, error: 'Error: Could not connect to the server. Please try again later.' }));
      console.error('Error updating notification preference:', error);
    }
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-[#453c5e] via-[#b398c0] to-[#7c4d8f] p-6">
      <h2 
        className="text-5xl md:text-6xl font-bold text-white mb-8 text-center"
        style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)' }} // Text shadow added here
      >
        Welcome, {profile.rollNo}!
      </h2>
      {profile.error && <p className="text-red-500 mb-4 text-center">{profile.error}</p>}

      <div className="bg-white p-10 rounded-2xl shadow-lg max-w-lg w-full text-left transform transition duration-500 hover:scale-105">
        <p className="text-lg font-semibold text-gray-800 mb-6">Roll No: {profile.rollNo}</p>

        {/* Custom CSS */}
        <style>
          {`
            input[type="checkbox"]:focus {
              outline: none; /* Removes the default outline */
              box-shadow: none; /* Removes any box-shadow that might appear */
            }
          `}
        </style>

        {/* Main Notifications Toggle */}
        <div className="flex items-center justify-between mb-6">
          <span className="text-lg text-gray-800">Enable Notifications</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={mainNotificationsEnabled}
              onChange={handleMainToggle}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-gray-200 rounded-full dark:bg-gray-700 peer-checked:bg-[#5b2a6e]"></div>
            <span className="absolute top-[2px] left-[2px] bg-white w-5 h-5 rounded-full transition-transform duration-300 peer-checked:translate-x-full peer-checked:border-white dark:border-gray-600"></span>
          </label>
        </div>

        {/* Individual Notifications Toggles */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Notification Preferences</h3>
          {['attendance', 'marks', 'timetable', 'seatingArrangement', 'results'].map((type) => (
            <div key={type} className="flex items-center justify-between mb-2">
              <span className="text-lg text-gray-800 capitalize">{type.replace(/([A-Z])/g, ' $1')}</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={mainNotificationsEnabled ? profile.notifications[type] : false}
                  onChange={() => handleToggleNotification(type)}
                  disabled={!mainNotificationsEnabled}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 rounded-full dark:bg-gray-700 peer-checked:bg-[#5b2a6e]"></div>
                <span className="absolute top-[2px] left-[2px] bg-white w-5 h-5 rounded-full transition-transform duration-300 peer-checked:translate-x-full peer-checked:border-white dark:border-gray-600"></span>
              </label>
            </div>
          ))}
        </div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="relative inline-flex items-center justify-center w-full py-4 px-6 text-lg font-bold text-white bg-[#5b2a6e] rounded-lg shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-[#362e49]/50 border border-[#5b2a6e] group"
        >
          <span className="relative z-10">Logout</span>
          <div className="absolute inset-0 bg-gradient-to-r from-[#362e49] to-[#5b2a6e] opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out"></div>
          <div className="absolute inset-0 w-1/2 bg-white opacity-10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-500 ease-in-out"></div>
        </button>
      </div>
    </div>
  );
};

export default Welcome;
