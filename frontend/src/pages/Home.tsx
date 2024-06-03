import type { Component } from "solid-js";
import Navbar from "../components/Navbar";
import Greeting from "../components/Greeting";
import LoadingScreen from "./Landing";

const Home: Component = () => {
  return (
    <div>
      <Navbar />
      <div class="m-2 p-0">
        <Greeting />
      </div>
      <main>
        <div class="grid grid-rows-12 lg:grid-rows-1 lg:grid-cols-12 gap-2 m-2 bg-base-200 rounded-lg p-2 lg:divide-x-2 divide-base-300">
          <div class="lg:col-span-3 row-span-3 lg:row-span-12">... orgs</div>
          <div class="lg:col-span-9 row-span-9 lg:row-span-12 flex flex-wrap p-2 gap-1">
            ... teams
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
