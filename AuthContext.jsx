import React, { createContext, useContext, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { toast } from '@/components/ui/use-toast';
import ApiService from '@/services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const { t } = useTranslation();

  useEffect(() => {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      setIsAuthenticated(true);
    }
    setLoading(false);
    
    // Demo kullanıcıları başlat
    initializeDemoData();
  }, []);

  const initializeDemoData = async () => {
    try {
      await ApiService.initDemoUsers();
      await ApiService.initDemoPromos();
    } catch (error) {
      console.error('Failed to initialize demo data:', error);
    }
  };

  const login = async (username, password) => {
    try {
      setLoading(true);
      const response = await ApiService.login(username, password);
      
      if (response.user) {
        setUser(response.user);
        setIsAuthenticated(true);
        localStorage.setItem('currentUser', JSON.stringify(response.user));
        toast({
          title: t('login.success'),
          description: t('login.welcome', { name: response.user.name }),
        });
        return response.user;
      }
    } catch (error) {
      toast({
        title: t('login.error'),
        description: error.message || t('login.invalid_credentials'),
        variant: "destructive",
      });
      return null;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('currentUser');
    toast({
      title: t('logout.success'),
      description: t('logout.description'),
    });
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};