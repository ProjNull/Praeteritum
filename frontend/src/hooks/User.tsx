import { KindeClient, KindeUser } from "@kinde-oss/kinde-auth-pkce-js";
import { getKindleClient } from "./Auth";
import { createSignal } from "solid-js";

const kinde: KindeClient = await getKindleClient();
const kindeUser: KindeUser | undefined = await kinde.getUserProfile();


const [fullname, setFullname] = createSignal("");
const familyName = (kindeUser?.family_name ?? "");
const givenName = (kindeUser?.given_name ?? "Anon");
setFullname(familyName == "" ? givenName : givenName + " " + familyName);

const [email, setEmail] = createSignal("");
setEmail(kindeUser?.email ?? "");

export { fullname, email };
