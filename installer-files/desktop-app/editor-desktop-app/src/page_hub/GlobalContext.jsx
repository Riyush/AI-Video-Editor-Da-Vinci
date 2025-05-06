// GlobalContext.jsx
import React, { createContext, useState } from "react";

export const GlobalContext = createContext();

export function GlobalProvider({ children }) {
  const [stripeSessionId, setStripeSessionId] = useState(null);
  const [userId, setUserId] = useState(null);

  return (
    <GlobalContext.Provider value={{
      stripeSessionId, setStripeSessionId,
      userId, setUserId
    }}>
      {children}
    </GlobalContext.Provider>
  );
}
