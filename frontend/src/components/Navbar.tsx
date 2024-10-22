import React from "react";
import { FaFacebook } from "react-icons/fa";
import { FaSquareXTwitter } from "react-icons/fa6";
import { AiFillInstagram } from "react-icons/ai";
import { FaPhoneAlt } from "react-icons/fa";
import { FaYoutube } from "react-icons/fa6";

const Navbar: React.FC = () => {
  return (
    <div className="flex justify-between items-center p-4 border-b">
      <div className="flex items-center space-x-4">
        <button className="text-xl">☰</button>
        <div className="flex items-center space-x-1">
          <span>English</span>
          <span>|</span>
          <span className="text-orange-500">ગુજરાતી</span>
        </div>
      </div>
      <div>
        <h1>
          <span className="text-black font-extrabold text-3xl dark:text-white">
            CMO
          </span>{" "}
          <span className="text-orange-500 font-extrabold text-3xl">
            GRIEVANCE PILOT TESTING
          </span>
        </h1>
      </div>
      <div className="flex items-center space-x-4">
        <button className="bg-black text-white rounded-full w-6 h-6 flex items-center justify-center">
          A
        </button>
        <button className="bg-gray-300 rounded-full w-6 h-6 flex items-center justify-center">
          A
        </button>
        <span>|</span>
        <div className="flex gap-2">
          <span>
            <FaPhoneAlt />
          </span>
          <span>+91 7923250073 - 74</span>
        </div>
        <span>|</span>
        <button className="text-xl flex gap-2 justify-center items-center">
          <span>A</span>
          <span className="bg-black rounded-full text-white flex items-center justify-center w-4 h-4 text-xl">
            +
          </span>
        </button>
        <button className="text-xl flex gap-2 justify-center items-center">
          A{" "}
          <span className="bg-black rounded-full text-white flex items-center justify-center w-4 h-4 text-xl">
            -
          </span>
        </button>
        <span>|</span>
        <button>
          <FaFacebook />
        </button>
        <button>
          <FaYoutube />
        </button>
        <button>
          <FaSquareXTwitter />
        </button>
        <button>
          <AiFillInstagram size={22} />
        </button>
      </div>
    </div>
  );
};

export default Navbar;
