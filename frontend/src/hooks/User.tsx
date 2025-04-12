import { createComputed, createSignal } from "solid-js";
import { authenticated } from "./Auth";

const [fullname, setFullname] = createSignal("");
const [email, setEmail] = createSignal("");
const [userid, setUserid] = createSignal("");

const updateUserData = async () => {
  const token = localStorage.getItem("token") ?? "";
  if (token == "") {
    return;
  }
  const resp = await fetch("/api/v1/kinde/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (resp.status != 200 || resp.redirected) {
    return;
  }
  const userData = await resp.json();
  const giveName = userData?.given_name ?? "Anon";
  const familyName = userData?.family_name ?? "";
  const fullUser = familyName == "" ? giveName : giveName + " " + familyName;
  const email = userData?.email ?? "";
  setEmail(email);
  setFullname(fullUser);
  setUserid(userData?.id ?? "");
};

createComputed(async () => {
  if (!authenticated()) {
    return;
  } else {
    await updateUserData();
  }
});

export { fullname, email, userid };
