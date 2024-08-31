import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Welcome = () => {
  const location = useLocation();
  const [profile, setProfile] = useState(location.state || { rollNo: '', notifications: false });
  const [error, setError] = useState('');

  useEffect(() => {
    if (!location.state) {
      const fetchProfile = async () => {
        try {
          const response = await fetch(`http://localhost:3000/profile?rollNo=${profile.rollNo}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (response.status === 200) {
            const data = await response.json();
            setProfile(data);
          } else {
            setError('Failed to load profile. Please try again later.');
          }
        } catch (error) {
          setError('Error: Could not connect to the server. Please try again later.');
          console.error('Error fetching profile:', error);
        }
      };

      fetchProfile();
    }
  }, [location.state, profile.rollNo]);

  const handleToggleNotifications = async () => {
    try {
      const updatedPreference = !profile.notifications;
      const response = await fetch('http://localhost:3000/notifications', {
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
        setError('Failed to update notification preference.');
      }
    } catch (error) {
      setError('Error: Could not connect to the server. Please try again later.');
      console.error('Error updating notification preference:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-green-400">
      <h2 className="text-4xl font-bold text-white mb-6">Welcome, {profile.rollNo}!</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="bg-white p-10 rounded-2xl shadow-2xl max-w-md w-full text-center">
        <p className="text-lg font-medium text-gray-800">Roll No: {profile.rollNo}</p>
        <div className="mt-6">
          <label className="flex items-center justify-center space-x-3">
            <input
              type="checkbox"
              checked={profile.notifications}
              onChange={handleToggleNotifications}
              className="form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out"
            />
            <span className="text-gray-700 text-lg">Receive Notifications</span>
          </label>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
