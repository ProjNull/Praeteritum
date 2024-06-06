import { createEffect, type Component, createComputed, createSignal, Show, JSXElement, createContext } from "solid-js";
import Navbar from "../components/Navbar";
import { fullname } from "../hooks/User";
import { useParams, action } from "@solidjs/router";
import { token } from "../hooks/Auth";

interface Retro {
  retro_id: number;
  stage: number;
  is_active: boolean;
  name: string;
  desc: string;
  is_public: boolean;
  group_id: number;
  user_id: string;
  display_type: number;
  columns: string[]
}

interface INote {
  note_id: number;
  user_id: string;
  retro_id: number;
  content: string;
  column: number;
}

interface Column {
  column_id: number;
  name: string;
  notes: INote[];
}

const mockData: Retro[] = [
  {
    'retro_id': 1,
    'group_id': 1,
    'user_id': "kp_f24f5b13426d40a7b534b2a168b500e0",
    'name': "My First Retrospective",
    'desc': "This is my first retrospective",
    'columns': ["Good", "Neutral", "Bad"],
    'display_type': 0,
    'stage': 1,
    'is_active': true,
    'is_public': false,
  }
];

const mockNotesData: INote[][] = [
  [
    {
      'note_id': 1,
      'user_id': 'kp_f24f5b13426d40a7b534b2a168b500e0',
      'retro_id': 1,
      'content': 'This is my first note',
      'column': 0
    },
    {
      'note_id': 2,
      'user_id': 'kp_f24f5b13426d40a7b534b2a168b500e0',
      'retro_id': 1,
      'content': 'This note starts in the middle column',
      'column': 1
    },
    {
      'note_id': 3,
      'user_id': 'kp_f24f5b13426d40a7b534b2a168b500e0',
      'retro_id': 1,
      'content': 'This note also starts in the middle column, below the previous one',
      'column': 1
    },
    {
      'note_id': 4,
      'user_id': 'kp_f24f5b13426d40a7b534b2a168b500e0',
      'retro_id': 1,
      'content': 'This note starts in the right column',
      'column': 2
    }
  ]
];

class Board implements Retro {
  retro_id: number;
  group_id: number;
  user_id: string;
  name: string;
  desc: string;
  columns: string[];
  display_type: number;
  stage: number;
  is_active: boolean;
  is_public: boolean;
  notes: INote[];
  constructor() {
    /*
     * Call the async method Board.finalize() to fetch data from remote
     */
    this.retro_id = 0;
    this.group_id = 0;
    this.user_id = "";
    this.name = "";
    this.desc = "";
    this.columns = [];
    this.display_type = 0;
    this.stage = 0;
    this.is_active = true;
    this.is_public = false;
    this.notes = [];
  }
  async finalize(retro_id: number) {
    const response = await fetch("/api/v1/retrospectives/get_retro_by_id", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token()}`,
      },
      body: JSON.stringify({
        retro_id: retro_id,
      }),
    });
    if (response.status == 500) {
      console.log("Got an internal server error while fetching a retro from remote");
      return;
    }
    if (response.status != 200 || response.redirected) {
      console.log("Response status mismatch, got: " + response.status + ", expected: 200\n(Line 66 pages/RetroView.tsx)\nMost likely, the retro either doesn't exist or we don't have permissions.");
      return;
    }
    await response.json().then((data) => {
      this.retro_id = data.retro_id;
      this.group_id = data.group_id;
      this.user_id = data.user_id;
      this.name = data.name;
      this.desc = data.desc;
      this.columns = data.columns;
      this.display_type = data.display_type;
      this.stage = data.stage;
      this.is_active = data.is_active;
      this.is_public = data.is_public;
    });
  }
  async fetch_notes() {
    const response = await fetch("/api/v1/notes/get_notes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token()}`,
      },
      body: JSON.stringify({
        retro_id: this.retro_id,
      }),
    });
    if (response.status == 500) {
      console.log("Got an internal server error while fetching notes from remote for retro " + this.retro_id);
      return;
    }
    if (response.status != 200 || response.redirected) {
      console.log("Response status mismatch, got: " + response.status + ", expected: 200\n(Line 66 pages/RetroView.tsx)\nMost likely, the retro either doesn't exist or we don't have permissions.");
      return;
    }
    await response.json().then((data) => {
      this.notes = data;
    });
  }
  get_column(column_id: number): Column {
    const column: Column = {
      column_id: column_id,
      name: this.columns[column_id],
      notes: this.notes.filter(note => note.column == column_id),
    }
    return column;
  }
  get_columns(): Column[] {
    return this.columns.map((column) => this.get_column(this.columns.indexOf(column)));
  }
}

interface NoteProps {
  note: INote;
  displayRefresh: () => void;
}

const NoteControls: Component<NoteProps> = ({ note, displayRefresh }) => {
  /*
    <button onclick={() => { console.log("Group is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 3.75H6.912a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859M12 3v8.25m0 0-3-3m3 3 3-3" />
      </svg>
    </button>
    <button onclick={() => { console.log("Move down is not mplemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor" class="size-6">
        <path stoke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h9.75m4.5-4.5v12m0 0-3.75-3.75M17.25 21 21 17.25" />
      </svg>
    </button>
    <button onclick={() => { console.log("Move up is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor" class="size-6">
        <path stoke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h5.25m5.25-.75L17.25 9m0 0L21 12.75M17.25 9v12" />
      </svg>
    </button>
    <button onclick={() => { console.log("Move column is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21 3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
      </svg>
    </button>
    <button onclick={() => { console.log("Edit is not implemented") }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
      </svg>
    </button>
  */
  return <>
    <button onclick={async () => {
      const res = await fetch("/api/v1/notes/remove_note", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token()}`,
        },
        body: JSON.stringify({
          note_id: note.note_id
        }),
      })

      if (res.ok) {
        await displayRefresh();
      } else {
        console.log(res);
        alert("Something went wrong! Check the console for details.")
      }
    }}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor" class="size-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
      </svg>
    </button>
  </>
}

const Note: Component<NoteProps> = ({ note, displayRefresh }) => {
  return <li>
    <div class="flex flex-row gap-1 grow justify-between">
      <div class="text-sm italic">{note.user_id}</div>
      <div>
        <NoteControls note={note} displayRefresh={displayRefresh} />
      </div>
    </div>
    <div><p>{note.content}</p></div>
  </li>
}

function generateRetroDisplay(retro: Board, setter: (n: number) => void, setRetroDisplay: (e: JSXElement) => void) {
  return <>{retro.get_columns().map((column: Column) => (
    <div id={column.name.toLowerCase()} class={"flex flex-col gap-2 grow rounded-lg py-2" + (column.column_id % 2 === (retro.columns.length % 2 === 1 ? 0 : 1) ? " bg-base-300" : "")}>
      <div class="text-2xl text-center">{column.name}</div>
      <hr class="border-2 mx-2 border-slate-500 rounded-lg" />
      <div class="mx-2">
        <ul class="gap-1 flex flex-col">
          {column.notes.map((note) => (
            <div class={"rounded-md p-1 " + (note.column % 2 === 0 ? "bg-secondary" : "bg-primary")}>
              <Note note={note} displayRefresh={async () => { await retro.fetch_notes(); setTimeout(() => { setRetroDisplay(generateRetroDisplay(retro, setter)); }, 100); }} />
            </div>
          ))}
        </ul>
      </div>
      <div class="mx-2 hidden sm:block">
        <div class="justify-center w-full flex">
          <button class="grow btn btn-ghost" onclick={() => { setter(column.column_id); }}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  ))}</>
}

interface NoteCreateModalProps {
  retroId: number;
  retro: Board;
  getter: () => number;
  setter: (n: number) => void;
  displaySetter: () => void;
}


interface CreateNoteData {
  column: number;
  content: string;
}

async function createNote(data: CreateNoteData, retroId: number, token: string) {
  try {
    const res = await fetch("/api/v1/notes/add_note", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        ...data,
        retro_id: retroId
      }),
    });
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Error ${res.status}: ${errorText}`);
    }
  } catch (error) {
    console.error("Error creating note:", error);
    alert("Something went wrong while creating a note. Check the console for details.");
  }
}

const NoteCreateModal: Component<NoteCreateModalProps> = ({ retroId, retro, getter, setter, displaySetter }) => {
  const [column, setColumn] = createSignal<number | null>(null);
  const [content, setContent] = createSignal<string>("");

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    if (column() !== null && content().trim()) {
      await createNote({
        column: column()!,
        content: content()
      }, retroId, token());
      setter(-1);
    } else {
      alert("Please fill in all fields.");
    }
  };

  createComputed(() => {
    if (getter() >= 0) {
      setColumn(getter());
    }
  })

  let options: JSXElement;
  createComputed(() => {
    getter()
    options = retro.get_columns().map(column => (
      <option value={column.column_id} selected={getter() === column.column_id}>{column.name}</option>
    ));
    console.log(options)
  });

  return (
    <>
      <Show when={getter() != -1}>
        <div class="absolute z-10 top-0 left-0 h-full w-full bg-black backdrop-blur-lg bg-opacity-20">
          <div class="flex flex-col items-center justify-center min-h-[100vh]">
            <div class="card w-96 bg-base-100 shadow-xl">
              <div class="card-body">
                <form onSubmit={async (e) => { await handleSubmit(e); await retro.fetch_notes(); displaySetter(); }}>
                  <h2 class="card-title">Add a new Note</h2>
                  <div class="flex flex-col flex-wrap gap-2">
                    <select
                      name="column"
                      class="select select-bordered w-full max-w-xs"
                      value={column() || ""}
                      onInput={(e) => setColumn(parseInt(e.currentTarget.value))}
                    >
                      <option disabled selected={getter() === -2} value={0}>Select a column</option>
                      {options}
                    </select>
                    <textarea
                      name="content"
                      class="textarea textarea-bordered"
                      placeholder="Card Heading\nDescription..."
                      value={content()}
                      onInput={(e) => setContent(e.currentTarget.value)}
                    />
                  </div>
                  <div class="card-actions justify-end">
                    <button
                      type="button"
                      class="btn btn-outline"
                      onClick={() => setter(-1)}
                    >
                      Close
                    </button>
                    <button
                      type="submit"
                      class="btn btn-success btn-outline"
                    >
                      Confirm
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </>
  );
};

const RetroView: Component = () => {
  const params = useParams();
  const retroId = parseInt(params.retro as string);
  const retro: Board = new Board();
  const [showCreateModal, setShowCreateModal] = createSignal(-1);
  const [retroDisplay, setRetroDisplay] = createSignal(<></>);
  createEffect(async () => { await retro.finalize(retroId); await retro.fetch_notes(); console.log(retro); setRetroDisplay(generateRetroDisplay(retro, setShowCreateModal, setRetroDisplay)); });
  return (
    <>
      <Navbar />
      <NoteCreateModal retroId={retroId} retro={retro} getter={showCreateModal} setter={setShowCreateModal} displaySetter={() => { setRetroDisplay(generateRetroDisplay(retro, setShowCreateModal)); }} />
      <main>
        <div class="m-2 block sm:hidden">
          <div class="justify-center w-full flex">
            <button class="grow btn btn-ghost" onclick={() => { setShowCreateModal(-2); }}>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>Create new note
            </button>
          </div>
        </div>
        <div class="flex flex-row gap-2 flex-wrap m-2">
          {retroDisplay()}
        </div>
      </main>
    </>
  );
};

export default RetroView;
