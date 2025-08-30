import './App.css';
import React, { FC, useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { Home, Login, Register } from './components/index.ts';
import { isAuthenticated } from './utils/Auth.ts';
import { AuthContext } from './utils/Auth.ts';

export const AuthContextApp = AuthContext;

export const App: FC = () => {
  const [authenticated, setAuthentication] =
    useState<boolean>(isAuthenticated());

  return (
    <AuthContextApp.Provider value={{ authenticated, setAuthentication }}>
      <BrowserRouter basename="/">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </AuthContextApp.Provider>
  );
};
