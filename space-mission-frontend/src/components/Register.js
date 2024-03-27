import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../css/login.css';
import spaceship from '../images/rocket-img.jpg';

function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '', 
    email: '',
    password: '',
    userType: '',
    nationality: '',
    age: '',
    education: '',
    weight: '',
    height: '',
    vocation: '',
    securityClearance: '',
    country: '',
    valuation: '',
    numberOfEmployees: '',
    budget: ''
  });
  const [message, setMessage] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  function updateForm(value) {
    return setForm((prev) => {
      return { ...prev, ...value };
    });
  }

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

  async function register(e){
    e.preventDefault();
    if(form.password !== confirmPassword){
      toast.error("Passwords do not match", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      setConfirmPassword('');
      return;
    } else {
      await axios.post('http://localhost:8000/signup/', form)
        .then(response => {
          setMessage(response.data.message);
          if (message === 'Logged in!') {
            navigate('/home'); // Redirect to Home page
          } else {
            updateForm({ username: '', password: '' });
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
    }
  };

  return (
    <div>
        <div class="login-container">
            <div class="left-column">
            <img src= {spaceship} alt="Login Image"/>
            </div>
            <div class="right-column">
            <h2>Register</h2>
            <form onSubmit={register} method="post">
                <div class="form-group">
                <label for="username">Name:</label>
                <input type="text" value={form.username} onChange={e => updateForm({username: e.target.value})} placeholder="Name" required/>
                </div>
                <div class="form-group">
                <label for="email">E-Mail:</label>
                <input type="text" value={form.email} onChange={e => updateForm({email: e.target.value})} placeholder="E-Mail" required/>
                </div>
                <div class="form-group" style={{display: "flex", alignItems: "center"}}>
                <label>User Type:</label>
                <div>
                    <label>
                        <input type="radio" value="Astronaut" checked={form.userType === 'Astronaut'} onChange={e => updateForm({userType: e.target.value})} />
                        Astronaut
                    </label>
                </div>
                <div>
                    <label>
                        <input type="radio" value="Organization" checked={form.userType === 'Organization'} onChange={e => updateForm({userType: e.target.value})} />
                        Organization
                    </label>
                </div>
                <div>
                    <label>
                        <input type="radio" value="Admin" checked={form.userType === 'Admin'} onChange={e => updateForm({userType: e.target.value})} />
                        Admin
                    </label>
                </div>
                </div>
                {form.userType === 'Astronaut' && (
                  <div className='right-column'>
                  <div class="form-group">
                  <label for="nationality">Nationality:</label>
                  <input type="text" value={form.nationality} onChange={e => updateForm({nationality: e.target.value})} placeholder="Nationality" required/>
                  </div>
                  <div class="form-group">
                  <label for="age">Age:</label>
                  <input type="text" value={form.age} onChange={e => updateForm({age: e.target.value})} placeholder="Age" required/>
                  </div>
                  <div class="form-group">
                  <label for="education">Education:</label>
                  <input type="text" value={form.education} onChange={e => updateForm({education: e.target.value})} placeholder="Education" required/>
                  </div>
                  <div class="form-group">
                  <label for="weight">Weight:</label>
                  <input type="text" value={form.weight} onChange={e => updateForm({weight: e.target.value})} placeholder="Weight" required/>
                  </div>
                  <div class="form-group">
                  <label for="height">Height:</label>
                  <input type="text" value={form.height} onChange={e => updateForm({height: e.target.value})} placeholder="Height" required/>
                  </div>
                  <div class="form-group">
                  <label for="vocation">Vocation:</label>
                  <input type="text" value={form.vocation} onChange={e => updateForm({vocation: e.target.value})} placeholder="Vocation" required/>
                  </div>
                  <div class="form-group">
                  <label for="securityClearance">Security Clearance:</label>
                  <input type="text" value={form.securityClearance} onChange={e => updateForm({securityClearance: e.target.value})} placeholder="Security Clearance" required/>
                  </div>
                  </div>
                )}
                {form.userType === 'Organization' && (
                  <div className='right-column'>
                  <div class="form-group">
                  <label for="country">Country:</label>
                  <input type="text" value={form.country} onChange={e => updateForm({country: e.target.value})} placeholder="Country" required/>
                  </div>
                  <div class="form-group">
                  <label for="valuation">Valuation:</label>
                  <input type="text" value={form.valuation} onChange={e => updateForm({valuation: e.target.value})} placeholder="Valuation" required/>
                  </div>
                  <div class="form-group">
                  <label for="numberOfEmployees">Number of Employees:</label>
                  <input type="text" value={form.numberOfEmployees} onChange={e => updateForm({numberOfEmployees: e.target.value})} placeholder="Number of Employees" required/>
                  </div>
                  <div class="form-group">
                  <label for="budget">Budget:</label>
                  <input type="text" value={form.budget} onChange={e => updateForm({budget: e.target.value})} placeholder="Budget" required/>
                  </div>
                  </div>
                )}
                <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" value={form.password} onChange={e => updateForm({password: e.target.value})} placeholder="Password" required/>
                </div>
                <div class="form-group">
                <label for="password">Confirm Password:</label>
                <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} placeholder="Confirm Password" required/>
                </div>
                <button type="submit">Register</button>
            </form>
            </div>
        </div>
    </div>
  );
}

export default Login;