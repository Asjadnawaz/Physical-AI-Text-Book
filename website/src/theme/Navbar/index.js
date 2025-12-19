import React from 'react';
import Navbar from '@theme-original/Navbar';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function CustomNavbar() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <>
      <div className="navbar-announcement">
        <div className="container">
          <div className="navbar-announcement-inner">
            📘 <strong>New Chapter Added:</strong> Check out Chapter 3 on Locomotion and Movement
          </div>
        </div>
      </div>
      <Navbar />
    </>
  );
}

export default CustomNavbar;