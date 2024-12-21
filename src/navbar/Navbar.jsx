import React from 'react';
import { NavLink } from 'react-router-dom';  // Using NavLink for route navigation

const Navbar = () => {
  return (
    <nav className="sticky bg-white top-0 flex justify-start items-center h-[75px] text-[20px] font-extrabold" id="navbar">
      <div className='flex w-[40%] justify-start pl-6'>
        <div className='flex rounded-full object-cover overflow-hidden'>
          <img src='../../public/assets/medilize_logo.jpg' className='h-[60px]'/>
        </div>
      </div>
      <div className='flex gap-[100px] ml-6 items-center relative navbarElements'>
        <NavLink to="/home" activeClassName="text-blue-500" id='nav-home'>Home</NavLink>
        <NavLink to="/patient" activeClassName="text-blue-500" id = 'nav-patient'>Patient</NavLink>
      </div>
      
    </nav>
  );
};

export default Navbar;
