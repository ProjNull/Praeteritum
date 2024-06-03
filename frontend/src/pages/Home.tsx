import type { Component } from "solid-js";
import { fullname, email } from "../hooks/User";
import Navbar from "../components/Navbar";

const Home: Component = () => {
  return (
    <div>
      <Navbar />
      <h1 class="text-3xl">Hello {fullname()}!</h1>
      <p class="text-2xl">Welcome to Praeteritum.</p>
      <p>
        Your email address is <span class="code">{email()}</span>
      </p>
    </div>
  );
};

export default Home;
