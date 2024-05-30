import type { Component } from "solid-js";
import { Router, Route } from "@solidjs/router";
import Home from "./pages/Home";
import LoadingScreen from "./pages/Landing";

import authenticate from "./hooks/Auth";

const App: Component = () => {
  authenticate(window.location.pathname === "/");
  return (
    <Router>
      <Route path="/" component={LoadingScreen} />
      <Route path="/home" component={Home} />
    </Router>
  );
};

export default App;
