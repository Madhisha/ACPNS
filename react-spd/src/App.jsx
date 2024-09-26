import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
<<<<<<< HEAD
import Registration from './registration';
=======
import Registration from './temp';
>>>>>>> 706825f835f9c95d7fbe1760e24a8fceed24b753
import ThankYou from './ThankYou';
import Welcome from './Welcome';
import Home from "./Home";
import Navbar from './components/Navbar'; // Adjust path as necessary
import About from './About';
import Contact from './Contact';

// import Footer from './Footer';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/thank-you" element={<ThankYou />} />
        <Route path="/welcome" element={<Welcome />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </Router>
  );
}

export default App;
