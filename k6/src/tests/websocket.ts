import socketio from "k6/x/socketio";
import { check, sleep } from "k6";
import { Options } from "k6/options";
import { TermPost } from "../term/types.ts";
import { uuid } from "../utils/uuid.ts";
import { termList as restTermList } from "./rest.ts";
import { randomArrayItem } from "../utils/array.ts";

const RESPONSE_WAIT_TIME = 5;
const WEBSOCKET_URL = "ws://host.docker.internal:5000";

export const options: Options = {
  scenarios: {
    termList: {
      executor: "shared-iterations",
      exec: termFind.name,
      vus: 100,
      iterations: 1000,
    },
    termCreate: {
      executor: "shared-iterations",
      exec: termCreate.name,
      vus: 100,
      iterations: 1000,
    },
    termDelete: {
      executor: "shared-iterations",
      exec: termDelete.name,
      vus: 100,
      iterations: 1000,
    },
    termEdit: {
      executor: "shared-iterations",
      exec: termEdit.name,
      vus: 100,
      iterations: 1000,
    },
  },
};

export function termFind() {
  const list = restTermList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  socketio.connect(WEBSOCKET_URL);
  socketio.emit("get_term", JSON.stringify({ id: term.id }));
  check(true, { "emit get_term event": (v) => v === true });
  sleep(RESPONSE_WAIT_TIME);
  socketio.disconnect();
}

export function termCreate() {
  const t: TermPost = { name: uuid(), definition: uuid() };
  socketio.connect(WEBSOCKET_URL);
  socketio.emit("create_term", JSON.stringify(t));
  check(true, { "emit create_term event": (v) => v === true });
  sleep(RESPONSE_WAIT_TIME);
  socketio.disconnect();
}

export function termDelete() {
  const list = restTermList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  socketio.connect(WEBSOCKET_URL);
  socketio.emit("delete_term", JSON.stringify({ id: term.id }));
  check(true, { "emit delete_term event": (v) => v === true });
  sleep(RESPONSE_WAIT_TIME);
  socketio.disconnect();
}

export function termEdit() {
  const list = restTermList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  socketio.connect(WEBSOCKET_URL);
  socketio.emit(
    "edit_term",
    JSON.stringify({
      id: term.id,
      name: term.name,
      definition: uuid(),
    })
  );
  check(true, { "emit edit_term event": (v) => v === true });
  sleep(RESPONSE_WAIT_TIME);
  socketio.disconnect();
}

export default termFind;
