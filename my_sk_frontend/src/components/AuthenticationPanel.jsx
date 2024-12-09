import { useState } from 'react';
import { DefaultInput } from './Input.jsx';
import axios from 'axios';


const AuthenticationPanel = ({
  name,
  submitUrl,
  requestMethod,
  ...props
}) => {
  axios.defaults.baseURL = 'http://0.0.0.0:8000';

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [validationResult, setvalidationResult] = useState({
    authentication: ''
  });
  const [success, setSuccess] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const requestBody = {
      username: formData.username,
      password: formData.password,
      email: formData.email ? formData.email : null
    };
    const requestConfig = {
      headers: {
        'Content-Type': 'application/json'
      }
    };

    axios.request({
      method: requestMethod, 
      url: submitUrl, 
      data:requestBody, 
      config: requestConfig
    }).then((response) => {
      const token = response.data.access_token;
      
      if (token) {
        localStorage.setItem('authToken', token);
        setSuccess(`${name} successful!`);
        setvalidationResult((currentState) => {
          return { ...currentState, authentication: ""};
        });      
      } else {
        setSuccess('');
        setvalidationResult((currentState) => {
          return { ...currentState, authentication: `${name} failed (Server failure)`};
        });
      }
    }).catch((error) => {
      let errorMessage = 'An unexpected error occurred!';
      const rejected_response = error.response;

      if (rejected_response) {
          errorMessage = rejected_response.data.detail;
        }

        setSuccess('');
        setvalidationResult((currentState) => {
          return { ...currentState, authentication: errorMessage };
        });
    });
  }

  return (
    <div
      style={{ flexDirection: 'column', display: 'flex', alignItems: 'center' }}>
      <h2>{name}</h2>
      <form onSubmit={handleSubmit}>
        <DefaultInput
          type="username"
          name="username"
          label="Username"
          ExternalState={formData}
          setExternalState={setFormData}
          pattern="[a-zA-Z0-9_.\-]+"
          minLength="3"
          maxLength="20"
          required={true}
        />
        <DefaultInput
          type="email"
          name="email"
          label="Email"
          ExternalState={formData}
          setExternalState={setFormData}
        />
        <DefaultInput
          type="password"
          name="password"
          label="Password"
          ExternalState={formData}
          setExternalState={setFormData}
          pattern="[A-Za-z0-9@$!%*#?&]+"
          minLength="6"
          maxLength="128"
          required={true}
        />
        <button type="submit">{props.buttonName}</button>
        {validationResult.login === '' ? null : (
          <p style={{ color: 'red' }}>{validationResult.authentication}</p>
        )}
        {success == '' ? null : <p style={{ color: 'green' }}>{success}</p>}
      </form>
    </div>
  );
};


const Register = () => {
  return <AuthenticationPanel name="Register" submitUrl="/user/auth/register" requestMethod="post" buttonName="Registration"/>
}
const Login = () => {
  return <AuthenticationPanel name="Login" submitUrl="/user/auth/login" requestMethod="post" buttonName="Login"/>
}

export {Login, Register, AuthenticationPanel};
