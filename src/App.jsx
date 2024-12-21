import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Import BrowserRouter for routing
import Navbar from './Navbars/Navbar';
import Home from './pages/Home/Home';
import Patient from './pages/Patient/Patient';
import ChatbotComponent from './components/ChatbotComponent';

function App() {
  const [count, setCount] = useState(0);

  return (
    <Router> {/* Wrap the entire app with Router to enable routing */}
      <Navbar /> {/* Always displayed Navbar */}

      <main className='bg-[#f2efb1] w-full h-full'>
        <Routes>
          {/* Define your routes here */}
          <Route path="/home" element={<Home />} />
          <Route path="/patient" element={<Patient />} />
        </Routes>
        
        <div className='fixed right-0 bottom-0'>
          <ChatbotComponent />
        </div>
      </main>
    </Router>
  );
}

export default App;
