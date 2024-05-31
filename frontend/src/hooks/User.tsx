import { createSignal } from "solid-js";

const [fullname, setFullname] = createSignal("");
const [email, setEmail] = createSignal("");

(async () => {
  const resp = await fetch("/api/v1/kinde/me", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token") ?? ""}`,
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
})();

export { fullname, email };
