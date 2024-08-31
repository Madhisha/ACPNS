import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Welcome = () => {
  const location = useLocation(); // React Router hook to access location data
  const [profile, setProfile] = useState(location.state || { rollNo: '', notifications: false }); // Initialize state with passed data
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if state is not passed (direct access) and fetch from server
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
  }, [location.state]);

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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl font-semibold mb-6">Welcome, {profile.rollNo}!</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="bg-white p-8 rounded-lg shadow-lg">
        <p>Roll No: {profile.rollNo}</p>
        <div className="mt-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={profile.notifications}
              onChange={handleToggleNotifications}
              className="form-checkbox"
            />
            <span className="ml-2">Receive Notifications</span>
          </label>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
