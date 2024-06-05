import { A } from "@solidjs/router";
import { Component, createSignal } from "solid-js";
import { fullname } from "../hooks/User";
import SettingsModal from "./Settings";

interface UserProfileProps {
  settingsSetter: (value: boolean) => void;
}

const UserProfile: Component<UserProfileProps> = ({ settingsSetter }) => {
  return (
    <div class="dropdown dropdown-end">
      <div class="flex flex-row-reverse align-middle items-center gap-2">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
          <div class="w-10 rounded-full">
            <img
              class="align-middle"
              alt="Tailwind CSS Navbar component"
              src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg"
            />
          </div>
        </div>
        <div>{fullname()}</div>
      </div>
      <ul
        tabindex="0"
        class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52"
      >
        <li>
          <a class="justify-between">Profile</a>
        </li>
        <li>
          <a onClick={() => settingsSetter(true)}>Settings</a>
        </li>
        <li>
          <A href="/token" activeClass="active" end={true}>
            Developers
            <span class="badge">new</span>
          </A>
        </li>
        <li>
          <a
            onClick={async () => {
              const token = localStorage.getItem("token");
              await fetch("/api/v1/kinde/logout", {
                headers: {
                  Authorization: `Bearer ${token ?? ""}`,
                },
              });
              localStorage.removeItem("token");
              alert("Logged out!");
              window.location.href = "/api/v1/kinde/register";
            }}
          >
            Logout
          </a>
        </li>
      </ul>
    </div>
  );
};

const NavbarLinks: Component = () => {
  return (
    <>
      <li>
        <A href="/home" activeClass="active" end={true}>
          Home
        </A>
      </li>
      <li>
        <details>
          <summary>Parent</summary>
          <ul class="p-2">
            <li>
              <a>Submenu 1</a>
            </li>
            <li>
              <a>Submenu 2</a>
            </li>
          </ul>
        </details>
      </li>
      <li>
        <a>Item 3</a>
      </li>
    </>
  );
};

const Navbar: Component = () => {
  const [showSettings, setShowSettings] = createSignal(false);
  return (
    <>
    <nav>
      <div class="navbar bg-base-200">
        <div class="navbar-start">
          <div class="dropdown">
            <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h8m-8 6h16"
                />
              </svg>
            </div>
            <ul
              tabindex="0"
              class="menu menu-sm dropdown-content mt-3 z-[3] p-2 shadow bg-base-100 rounded-box w-52"
            >
              <NavbarLinks />
            </ul>
          </div>
          <ul class="menu menu-horizontal px-1 hidden z-10 lg:flex">
            <NavbarLinks />
          </ul>
          <a class="btn btn-ghost text-xl flex lg:hidden">Praeteritum</a>
        </div>
        <div class="navbar-center hidden lg:flex">
          <a class="btn btn-ghost text-xl">Praeteritum</a>
        </div>
        <div class="navbar-end">
          <UserProfile settingsSetter={setShowSettings} />
        </div>
      </div>
    </nav>
      <SettingsModal setter={setShowSettings} getter={showSettings}/>
    </>
  );
};

export default Navbar;
