import { useState, useEffect } from 'react'
import Auth from "./Auth"; 
import Dashboard from './Dashboard';
import './index.css';


    function App() {
        const [isLoggedIn, setIsLoggedIn] = useState(false);
        useEffect(() => {
          const token = localStorage.getItem('token');
          if (token) {
            setIsLoggedIn(true);
          }
        }, []);

    const handleLogout = () => {
          localStorage.removeItem('token');
          setIsLoggedIn(false);
        };

    if (!isLoggedIn) {
          return <Auth onLoginSuccess={() => setIsLoggedIn(true)} />
        }
          
          return (
              <div>
                  <nav className="navbar navbar-dark bg-dark px-4">
                      <span className="navbar-brand bg-dark mb-0 h1">DevTracker Dashboard</span>
                      <button className="btn btn-outline-danger btn-sm" onClick={handleLogout}>Logout</button>
                  </nav>

                  <div className="container mt-4">
                      <div className=" alert alert-success">
                          <h4 className='alert-success'>Welcome to DevTracker!</h4>
                          <p className="alert-success">Your productivity journey starts here.</p>
                      </div>
                      < Dashboard/>
                  </div>
              </div>
          );
      }

export default App;







