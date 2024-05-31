import { A } from "@solidjs/router";
import { Component } from "solid-js";
import { fullname } from "../hooks/User";

const Navbar: Component = () => {
  return (
    <nav>
      <div class="bg-base-600 flex flex-row gap-2 justify-between">
        <ul class="list-none">
          <li>
            <A href="/home">Home</A>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
