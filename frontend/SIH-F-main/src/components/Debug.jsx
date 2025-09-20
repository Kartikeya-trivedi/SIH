import React from 'react';

const Debug = () => {
  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Debug Page</h1>
      
      <section style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>Environment Information</h2>
        <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', overflowX: 'auto' }}>
          {JSON.stringify({
            NODE_ENV: import.meta.env.MODE,
            BASE_URL: import.meta.env.BASE_URL,
            DEV: import.meta.env.DEV,
            PROD: import.meta.env.PROD,
            apiUrl: import.meta.env.VITE_API_URL || 'not set',
            useMockData: import.meta.env.VITE_USE_MOCK_DATA || 'not set',
          }, null, 2)}
        </pre>
      </section>
      
      <section style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>Browser Information</h2>
        <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', overflowX: 'auto' }}>
          {JSON.stringify({
            userAgent: navigator.userAgent,
            language: navigator.language,
            cookiesEnabled: navigator.cookieEnabled,
            online: navigator.onLine,
            screenWidth: window.innerWidth,
            screenHeight: window.innerHeight,
          }, null, 2)}
        </pre>
      </section>
      
      <section style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>React Router Information</h2>
        <p>Current Location: <code>{window.location.pathname}</code></p>
        <p>Search Params: <code>{window.location.search}</code></p>
        <p>Hash: <code>{window.location.hash}</code></p>
      </section>
    </div>
  );
};

export default Debug;