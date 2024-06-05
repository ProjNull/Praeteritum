import { type Component } from "solid-js";
import Navbar from "../components/Navbar";
import { fullname } from "../hooks/User";
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

interface INote {
  note_id: number;
  column_index: number;
  author: string;
  content: string;
}

interface Column {
  column_id: number;
  name: string;
  notes: INote[];
}

interface NoteProps {
  note: INote;
}

const NoteControls: Component<NoteProps> = ({ note }) => {
  return <>
    <button onclick={() => { alert("Group is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 3.75H6.912a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859M12 3v8.25m0 0-3-3m3 3 3-3" />
      </svg>
    </button>
    <button onclick={() => { alert("Move down is not mplemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor" class="size-6">
        <path stoke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h9.75m4.5-4.5v12m0 0-3.75-3.75M17.25 21 21 17.25" />
      </svg>
    </button>
    <button onclick={() => { alert("Move up is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor" class="size-6">
        <path stoke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h5.25m5.25-.75L17.25 9m0 0L21 12.75M17.25 9v12" />
      </svg>
    </button>
    <button onclick={() => { alert("Move column is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21 3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
      </svg>
    </button>
    <button onclick={() => { alert("Edit is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
      </svg>
    </button>
    <button onclick={() => { alert("Delete is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor" class="size-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
      </svg>
    </button>
  </>
}

const Note: Component<NoteProps> = ({ note }) => {
  return <li>
    <div class="flex flex-row gap-1 grow justify-between">
      <div class="text-sm italic">{note.author}</div>
      <div>
        <NoteControls note={note} />
      </div>
    </div>
    <div><p>{note.content}</p></div>
  </li>
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
  const retroColumns: Column[] = [
    {
      column_id: 1,
      name: "Bad",
      notes: [
        {
          note_id: 1,
          content: "This is an example note",
          author: fullname(),
          column_index: 1,
        }
      ],
    },
    {
      column_id: 2,
      name: "OK",
      notes: [
        {
          note_id: 2,
          content: "This is another example note",
          author: fullname(),
          column_index: 1,
        }
      ],
    },
    {
      column_id: 3,
      name: "Good",
      notes: [
        {
          note_id: 3,
          content: "This is yet another example note",
          author: fullname(),
          column_index: 1,
        },
        {
          note_id: 4,
          content: "And this one is in the same column as the 3rd one!",
          author: fullname(),
          column_index: 2,
        }
      ],
    },
  ];
  const retro: Retro = mockRestros.filter((retro) => retro.retro_id == retroId)[0];
  return (
    <>
      <Navbar />
      <main>
        <div class="m-2 block sm:hidden">
          <div class="justify-center w-full flex">
            <button class="grow btn btn-ghost" onclick={() => { alert("Mobile fullscreen create is not implemented") }}>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
            </button>
          </div>
        </div>
        <div class="flex flex-row gap-2 flex-wrap m-2">
          {retroColumns.map((column) => (
            <div id={column.name.toLowerCase()} class={"flex flex-col gap-2 grow rounded-lg py-2" + (column.column_id % 2 === 1 ? " bg-base-300" : "")}>
              <div class="text-2xl text-center">{column.name}</div>
              <hr class="border-2 mx-2 border-slate-500 rounded-lg" />
              <div class="mx-2">
                <ul class="gap-1 flex flex-col">
                  {column.notes.map((note) => (
                    <div class={"rounded-md p-1 " + (note.column_index % 2 === 0 ? "bg-secondary" : "bg-primary")}>
                      <Note note={note} />
                    </div>
                  ))}
                </ul>
              </div>
              <div class="mx-2 hidden sm:block">
                <div class="justify-center w-full flex">
                  <button class="grow btn btn-ghost" onclick={() => { alert("Create is not implemented") }}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </>
  );
};

export default RetroView;
