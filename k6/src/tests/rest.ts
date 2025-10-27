import http from "k6/http";
import { check } from "k6";
import { Options } from "k6/options";
import { uuid } from "../utils/uuid.ts";
import { randomArrayItem } from "../utils/array.ts";
import { Term, TermPost } from "../term/types.ts";
import { isTerm } from "../term/isTerm.ts";

export const options: Options = {
  scenarios: {
    getTerm: {
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

export function termList() {
  const result = http.get("http://host.docker.internal:8000/term/list");
  const json = result.json();
  const isTermsList = Array.isArray(json) && json.every(isTerm);
  check(result, {
    "is status 200": (r) => r.status === 200,
    "is terms list": () => isTermsList,
  });
  if (!isTermsList) return [];
  const list = json as unknown as Term[];
  return list;
}

export function termFind() {
  const list = termList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  const termGetResult = http.get(
    `http://host.docker.internal:8000/term?id=${term.id}`
  );
  const isResultTerm = isTerm(termGetResult.json);
  check(termGetResult, {
    "is status 200": (r) => r.status === 200,
    "is terms": () => isResultTerm,
  });
}

export function termCreate() {
  const t: TermPost = { name: uuid(), definition: uuid() };
  const result = http.post(
    "http://host.docker.internal:8000/term",
    JSON.stringify(t),
    { headers: { "Content-Type": "application/json" } }
  );
  check(result, {
    "is status 200": (r) => r.status === 200,
    "is same term": (r) => {
      const b = r.json();
      return isTerm(b) && b.name === t.name && b.definition === t.definition;
    },
  });
}

export function termDelete() {
  const list = termList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  const result = http.del(
    "http://host.docker.internal:8000/term",
    JSON.stringify({ id: term.id }),
    { headers: { "Content-Type": "application/json" } }
  );
  check(result, {
    "is status 200": (r) => r.status === 200,
  });
}

export function termEdit() {
  const list = termList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  const result = http.patch(
    "http://host.docker.internal:8000/term",
    JSON.stringify({ id: term.id, name: term.name, definition: uuid() }),
    { headers: { "Content-Type": "application/json" } }
  );
  check(result, {
    "is status 200": (r) => r.status === 200,
  });
}

export default termFind;
