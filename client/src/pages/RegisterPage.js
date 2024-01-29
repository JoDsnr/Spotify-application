import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";
const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const registerUser = async () => {
    try {
      const resp = await httpClient.post("//localhost:5000/register", {
        email,
        password,
      });

      // Assuming the registration response includes a Spotify authorization URL
      const spotifyAuthorizationUrl = resp.data.spotifyAuthorizationUrl;

      // Redirect the user to Spotify for authorization
      window.location.href = spotifyAuthorizationUrl;
    } catch (error) {
      if (error.response.status === 401) {
        alert("Invalid credentials");
      }
    }
  };


  return (
    <div>
      <h1>Create an account</h1>
      <form>
        <div>
          <label>Email: </label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            id=""
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id=""
          />
        </div>
        <button type="button" onClick={() => registerUser()}>
          Submit
        </button>
      </form>
    </div>
  );
};

export default RegisterPage;
