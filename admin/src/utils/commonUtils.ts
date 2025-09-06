import { clearTokens } from '../services/Tokens.ts';

export const handleNavigate = (path: string) => {
    if (path === '/login') {
      clearTokens();
    }
    window.location.href = path;
  };
