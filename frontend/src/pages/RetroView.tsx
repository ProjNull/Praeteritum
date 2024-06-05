import { type Component } from "solid-js";
import Navbar from "../components/Navbar";
import Greeting from "../components/Greeting";
import { useParams } from "@solidjs/router";

interface Retro {
  retro_id: number;
  stage: number;
  is_active: boolean;
  name: string;
  description: string;
  is_public: boolean;
  organization_id: number;
  user_id: string;
}

const RetroView: Component = () => {
  const params = useParams();
  const retroId = parseInt(params.retro as string);
  const mockRestros: Retro[] = [
    {
      retro_id: 1,
      stage: 1,
      is_active: true,
      name: "Retro 1",
      description: "Description for Retro 1",
      is_public: true,
      organization_id: 1,
      user_id: "1",
    },
    {
      retro_id: 2,
      stage: 1,
      is_active: true,
      name: "Retro 2",
      description: "Description for Retro 2",
      is_public: true,
      organization_id: 1,
      user_id: "2",
    },
  ];
  const retro: Retro = mockRestros.filter((retro) => retro.retro_id == retroId)[0];
  return (
    <div>
      <Navbar />
      <main>
        {retro.name}
      </main>
    </div>
  );
};

export default RetroView;
