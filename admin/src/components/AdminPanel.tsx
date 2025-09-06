import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/AdminPanel.scss';
import NavBar from './NavBar.tsx';
import { handleNavigate } from '../utils/commonUtils.ts'

const AdminPanel: React.FC = () => {
  return (
    <div>
      <NavBar onNavigate={handleNavigate} isMainAdminPanel={true} />
      <h1>Admin Panel</h1>
      <nav>
        <ul>
          <li>
            <Link to="/users">Manage Users</Link>
          </li>
          <li>
            <Link to="/games">Manage Game Sessions</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default AdminPanel;
