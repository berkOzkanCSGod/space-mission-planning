import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/login.css';
import spaceship from '../images/rocket-img.jpg';

function Login() {
  const [message, setMessage] = useState('');

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

  const numStars = 100; // Adjust as needed
  const body = document.querySelector('body');
  for (let i = 0; i < numStars; i++) {
    const star = createStar();
    body.appendChild(star);
  }

  useEffect(() => {
    axios.get('http://localhost:8000/login/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
        <div class="login-container">
            <div class="left-column">
            <img src= {spaceship} alt="Login Image"/>
            </div>
            <div class="right-column">
            <h2>Login</h2>
            <form action="{% url 'login' %}" method="post">
                <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required/>
                </div>
                <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required/>
                </div>
                <button type="submit">Login</button>
            </form>
            </div>
        </div>
    </div>
  );
}

export default Login;