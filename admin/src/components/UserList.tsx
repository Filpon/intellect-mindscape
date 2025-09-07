import React, { useEffect, useState } from 'react';
import {
  fetchUsers,
  deleteUser,
} from '../services/userService.ts';
import UserForm from './UserForm.tsx';
import Spinner from './Spinner.tsx';
import '../styles/UserList.scss';
import { ModalWindow } from './common/ModalWindow.tsx';
import { ModalWindowConfirm } from './common/ModalWindowConfirm.tsx';
import NavBar from './NavBar.tsx';
import { handleNavigate } from '../utils/commonUtils.ts';

interface UserListProps {
  currentUserId: string | null;
}

const UserList: React.FC<UserListProps> = ({ currentUserId }) => {
  const [users, setUsers] = useState<
    Array<{ id: string; username: string; email: string }>
  >([]);
  const [selectedUser, setSelectedUser] = useState<{
    id: string;
    username: string;
    email: string;
  } | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [showModal, setShowModal] = useState(false);
  const [showModalConfirm, setShowModalConfirm] = useState(false);
  const [title, setTitle] = useState('Notification');
  const [message, setMessage] = useState('');
  const [userToDelete, setUserToDelete] = useState<string | null>(null);

  const fetchUsersList = async () => {
    try {
      setLoading(true);
      const data = await fetchUsers();
      // Ensure data is an array before setting state
      if (data && Array.isArray(data.users)) {
        setUsers(data.users);
      } else {
        console.error('Fetched data is empty:', data);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsersList();
  }, []);

  const handleDeleteConfirmation = async (userId: string) => {
    setUserToDelete(userId);
    setTitle('Confirmation');
    setMessage('Are you sure you want to delete this user?');
    setShowModalConfirm(true);
  };

  const handleDelete = async () => {
    if (userToDelete !== null) {
      try {
        await deleteUser(userToDelete);
        await fetchUsersList();
        setMessage('User was deleted successfully.');
        setShowModal(true);
      } catch (error) {
        setMessage('Failed to delete user. Please try again.');
      } finally {
        setShowModalConfirm(false);
      }
    }
  };

  return (
    <div>
      <NavBar onNavigate={handleNavigate} />
      <UserForm
        selectedUser={selectedUser}
        setSelectedUser={setSelectedUser}
        fetchUsersList={fetchUsersList}
      />

      {loading ? (
        <Spinner />
      ) : (
        <ul>
          {users.length > 0 ? (
            users.map((user) => (
              <li key={user.id}>
                {user.username} - {user.email}
                <button onClick={() => handleDeleteConfirmation(user.id)} disabled={user.id === currentUserId}>
                  Delete
                </button>
                <button onClick={() => setSelectedUser(user)}>Edit</button>
              </li>
            ))
          ) : (
            <li>No users found</li>
          )}
        </ul>
      )}
      <ModalWindow
        show={showModal}
        handleClose={() => setShowModal(false)}
        title={title}
        messageBody={message}
      />
      <ModalWindowConfirm
        show={showModalConfirm}
        handleClose={() => setShowModalConfirm(false)}
        title={title}
        messageBody={message}
        onConfirm={handleDelete}
      />
    </div>
  );
};

export default UserList;
