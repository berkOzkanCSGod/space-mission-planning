import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../css/login.css';
import spaceship from '../images/rocket-img.jpg';

function Login() {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  function randomInRange(min, max) {
    return Math.random() * (max - min) + min;
  }

  function createStar() {
    const star = document.createElement('div');
    star.classList.add('star');
    star.style.width = `${randomInRange(1, 4)}px`;
    star.style.height = star.style.width;
    star.style.top = `${randomInRange(0, 100)}%`;
    star.style.left = `${randomInRange(0, 100)}%`;
    star.style.animationDuration = `${randomInRange(2, 6)}s`;
    return star;
  }

  useEffect(() => {
    const numStars = 100; // Adjust as needed
    const body = document.querySelector('body');
    const stars = []; // Array to hold the star elements
  
    for (let i = 0; i < numStars; i++) {
      const star = createStar();
      body.appendChild(star);
      stars.push(star); // Add the star to the array
    }
  
    return () => {
      // Cleanup function to remove the stars
      stars.forEach(star => {
        body.removeChild(star);
      });
    };
  }, []);

  async function login(e){
    e.preventDefault();
    await axios.post('http://localhost:8000/login/', {username, password})
      .then(response => {
        setMessage(response.data.message);
        if (response.data.message === 'Logged in!') {
          navigate('/home'); // Redirect to Home page
        } else {
          setUsername('');
          setPassword('');
          toast.error(response.data.error_message, {
            position: "top-center",
            autoClose: 3000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
            });
        }
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div>
        <div class="login-container">
            <div class="left-column">
            <img src= {spaceship} alt="Login Image"/>
            </div>
            <div class="right-column">
            <h2>Login</h2>
            <form onSubmit={login} method="post">
                <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" required/>
                </div>
                <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required/>
                </div>
                <button type="submit">Login</button>
            </form>
            </div>
        </div>
    </div>
  );
}

export default Login;