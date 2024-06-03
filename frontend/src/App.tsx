import type { Component } from "solid-js";
import { Router, Route } from "@solidjs/router";

import { resolveAuthenticationToken, ready } from "./hooks/Auth";

import Home from "./pages/Home";

import LoadingScreen from "./pages/Landing";
import TokenDisplay from "./pages/Token";

const Void: Component = () => {
  return <></>;
};

await resolveAuthenticationToken();

const App: Component = () => {
  return (
    <>
      {!ready() && (
        <div class="absolute z-10 top-0 left-0 h-full w-full bg-black backdrop-blur-lg bg-opacity-20">
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
