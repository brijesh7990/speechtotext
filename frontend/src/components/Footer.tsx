import React from "react";

const Footer: React.FC = () => {
  return (
    <div className="flex justify-between items-center bg-orange-500 dark:bg-black text-white py-2 px-4">
      <span>
        Official Website of Chief Minister’s Office, Gujarat | Copyright © 2024
      </span>
      <div className="flex items-center">
        <span>Last Updated: 21 Oct, 2024</span>
        <span className="ml-4">Total views : 16457244</span>
      </div>
    </div>
  );
};

export default Footer;
