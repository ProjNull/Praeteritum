import type { Component } from "solid-js";
import { Router, Route } from "@solidjs/router";
import Home from "./pages/Home";
import LoadingScreen from "./pages/Landing";

const App: Component = () => {
  return (
    <Router>
      <Route path="/" component={LoadingScreen} />
      <Route path="/home" component={Home} />
    </Router>
  );
};

export default App;