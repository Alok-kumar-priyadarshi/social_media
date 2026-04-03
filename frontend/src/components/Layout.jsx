// This layout wraps all pages with sidebar

import Sidebar from "./Sidebar";

export default function Layout({ children }) {
  return (
    <div className="flex">
      
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="ml-60 w-full">
        {children}
      </div>

    </div>
  );
}