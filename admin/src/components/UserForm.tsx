import React, { useEffect, useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { handleRegister, updateUserById } from '../services/userService.ts';
import '../styles/UserForm.scss';
import { AxiosError } from 'axios';
import { ModalWindow } from './common/ModalWindow.tsx';

interface UserFormProps {
  selectedUser: any;
  setSelectedUser: (user: any) => void;
  fetchUsersList: () => Promise<void>;
}

const UserForm: React.FC<UserFormProps> = ({
  selectedUser,
  setSelectedUser,
  fetchUsersList,
}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState('Notification');
  const [message, setMessage] = useState('');
  const [isLoginDisabled, setIsLoginDisabled] = useState(false);
  const handleCloseModal = () => setShowModal(false);

  useEffect(() => {
    if (selectedUser) {
      setUsername(selectedUser.username);
      setPassword(selectedUser.password);
      setConfirmPassword('');
      setIsLoginDisabled(true);
    } else {
      setUsername('');
      setPassword('');
      setConfirmPassword('');
      setIsLoginDisabled(false);
    }
  }, [selectedUser]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');

    // Check if passwords match
    if (password !== confirmPassword) {
      setTitle('Error');
      setMessage('Passwords do not match. Please try again.');
      setShowModal(true);
      return;
    }

    if (selectedUser) {
      try {
        await updateUserById(selectedUser.id, password);
        await fetchUsersList(); // Calling fetchUsersList to refresh the user list
        setTitle('Notification');
        setMessage(`Successful update of ${selectedUser.username}!`);
        setShowModal(true);
      } catch (err) {
        const error = err as AxiosError; // Ensure error is typed correctly
        if (error.response && error.response.status === 500) {
          setMessage('Server connection error');
          setShowModal(true);
        } else if (error?.code === 'ECONNABORTED') {
          setMessage('Connection to server is not established');
          setShowModal(true);
        } else if (error?.code === 'ERR_NETWORK') {
          setMessage('Server domain network error');
          setShowModal(true);
        } else {
          setMessage('Something went wrong. Try later');
          setShowModal(true);
        }
      }
    } else {
      try {
        await handleRegister(username, password);
        await fetchUsersList(); // Call fetchUsersList to refresh the user list
        setTitle('Notification');
        setMessage('Successful registration!');
        setShowModal(true);
        setUsername('');
        setPassword('');
        setConfirmPassword('');
      } catch (err) {
        const error = err as AxiosError; // Ensure error is typed correctly
        console.error(error?.code);
        setTitle('Error');
        if (error.response && error.response.status === 409) {
          setMessage('Username already exists');
          setShowModal(true);
        } else if (error.response && error.response.status === 500) {
          setMessage('Server connection error');
          setShowModal(true);
        } else if (error?.code === 'ECONNABORTED') {
          setMessage('Connection to server is not established');
          setShowModal(true);
        } else if (error?.code === 'ERR_NETWORK') {
          setMessage('Server domain network error');
          setShowModal(true);
        } else {
          setMessage('Something went wrong. Try later');
          setShowModal(true);
        }
      }
    }
    setSelectedUser(null);
  };

  const handleCancel = () => {
    setSelectedUser(null);
    setIsLoginDisabled(false);
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <h3>{selectedUser ? 'Edit User' : 'New User'}</h3>
        <Form.Group controlId="formUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            disabled={isLoginDisabled} // Disable input if login is disabled
          />
        </Form.Group>
        <Form.Group controlId="formPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group controlId="formConfirmPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </Form.Group>
        <ModalWindow
          show={showModal}
          handleClose={handleCloseModal}
          title={title}
          messageBody={message}
        />
        <Button type="submit">{selectedUser ? 'Update' : 'Create'}</Button>
        {selectedUser && (
          <Button type="button" onClick={handleCancel}>
            Reset edit
          </Button>
        )}
      </Form>
    </>
  );
};

export default UserForm;
