import type { Component } from "solid-js";
import { Router, Route } from "@solidjs/router";

import { resolveAuthenticationToken, ready } from "./hooks/Auth";

import Home from "./pages/Home";

import LoadingScreen from "./pages/Landing";
import TokenDisplay from "./pages/Token";
import { getTheme } from "./hooks/Theme";

const Void: Component = () => {
  return <></>;
};

await resolveAuthenticationToken();

const App: Component = () => {
  console.log("Using the " + getTheme() + " theme at initialization.");
  return (
    <>
      {!ready() && (
        <div class="absolute z-20 top-0 left-0 h-full w-full bg-black backdrop-blur-lg bg-opacity-20">
          <LoadingScreen />
        </div>
      )}
      <Router>
        <Route path="/" component={Void} />
        <Route path="/home" component={Home} />
        <Route path="/token" component={TokenDisplay} />
      </Router>
    </>
  );
};

export default App;
