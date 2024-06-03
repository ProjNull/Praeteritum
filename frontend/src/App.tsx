import type { Component } from "solid-js";
import { Router, Route } from "@solidjs/router";

import { resolveAuthenticationToken } from "./hooks/Auth";

import Home from "./pages/Home";

import LoadingScreen from "./pages/Landing";
import TokenDisplay from "./pages/Token";

const App: Component = () => {
  resolveAuthenticationToken();
  return (
    <Router>
      <Route path="/" component={LoadingScreen} />
      <Route path="/home" component={Home} />
      <Route path="/token" component={TokenDisplay} />
    </Router>
  );
};

export default App;
