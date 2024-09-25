import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Welcome = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(location.state || { rollNo: '', notifications: {}, error: '' });
  const [mainNotificationsEnabled, setMainNotificationsEnabled] = useState(true); // Main toggle state

  useEffect(() => {
    if (!location.state) {
      const fetchProfile = async () => {
        try {
          const response = await fetch(`http://localhost:5000/profile?rollNo=${profile.rollNo}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (response.status === 200) {
            const data = await response.json();
            setProfile(data);
            setMainNotificationsEnabled(data.notifications.main || true); // Initialize main toggle
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
      const response = await fetch('http://localhost:5000/notifications', {
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
    
    // Update all individual preferences based on the main toggle
    const updatedNotifications = {
      attendance: updatedPreference,
      marks: updatedPreference,
      timetable: updatedPreference,
      seatingArrangement: updatedPreference,
      results: updatedPreference,
    };

    try {
      const response = await fetch('http://localhost:5000/notifications', {
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-purple-600 to-blue-500 p-6">
      <h2 className="text-5xl md:text-6xl font-bold text-white mb-8 text-center">Welcome, {profile.rollNo}!</h2>
      {profile.error && <p className="text-red-500 mb-4 text-center">{profile.error}</p>}
      
      <div className="bg-white p-10 rounded-2xl shadow-lg max-w-lg w-full text-left transform transition duration-500 hover:scale-105">
        <p className="text-lg font-semibold text-gray-800 mb-6">Roll No: {profile.rollNo}</p>

        {/* Main Notifications Toggle */}
        <div className="flex items-center justify-between mb-6">
          <span className="text-lg text-gray-800">Enable All Notifications</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={mainNotificationsEnabled}
              onChange={handleMainToggle}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:bg-blue-600"></div>
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
                  disabled={!mainNotificationsEnabled} // Disable individual toggles if main is off
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:bg-blue-600"></div>
                <span className="absolute top-[2px] left-[2px] bg-white w-5 h-5 rounded-full transition-transform duration-300 peer-checked:translate-x-full peer-checked:border-white dark:border-gray-600"></span>
              </label>
            </div>
          ))}
        </div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="mt-6 w-full py-3 bg-gradient-to-r from-red-500 to-pink-500 text-white text-lg font-semibold rounded-full shadow-lg hover:from-red-600 hover:to-pink-600 transform hover:scale-105 transition duration-300"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Welcome;
