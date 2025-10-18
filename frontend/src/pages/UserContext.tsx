// frontend/src/contexts/UserContext.tsx
import React, { createContext, useContext, useState, ReactNode } from "react";

export interface UserProfile {
    id: number;
    name: string;
    email: string;
    picture?: string;
}

interface UserContextType {
    user: UserProfile | null;
    setUser: (user: UserProfile | null) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<UserProfile | null>(null);

    return <UserContext.Provider value={{ user, setUser }}>{children}</UserContext.Provider>;
};

// Hook to use user context
export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) throw new Error("useUser must be used within a UserProvider");
    return context;
};
