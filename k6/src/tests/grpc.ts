import { check } from "k6";
import { Client, StatusOK } from "k6/net/grpc";
import { Options } from "k6/options";
import { isTerm } from "../term/isTerm.ts";
import { randomArrayItem } from "../utils/array.ts";
import { uuid } from "../utils/uuid.ts";
import { TermPost } from "../term/types.ts";

const client = new Client();
client.load(["/proto"], "term.proto");

export const options: Options = {
  scenarios: {
    termFind: {
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
  client.connect("host.docker.internal:50051", { plaintext: true });
  const response = client.invoke("/term.v1.TermService/List", {});
  const message = response.message;
  const isTermList = Array.isArray(message) && message.every(isTerm);
  check(response, {
    "is status OK": (r) => r && r.status === StatusOK,
    "is term list": () => isTermList,
  });
  client.close();
  if (!isTermList) return [];
  return message;
}

export function termFind() {
  const list = termList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  client.connect("host.docker.internal:50051", { plaintext: true });
  const response = client.invoke("/term.v1.TermService/Get", { id: term.id });
  const isResultTerm = isTerm(response.message);
  check(response, {
    "is status OK": (r) => r && r.status === StatusOK,
    "is term": () => isResultTerm,
  });
}

export function termCreate() {
  const t: TermPost = { name: uuid(), definition: uuid() };
  client.connect("host.docker.internal:50051", { plaintext: true });
  const result = client.invoke("/term.v1.TermService/Create", t);
  check(result, {
    "is status OK": (r) => r && r.status === StatusOK,
    "is same term": (r) =>
      isTerm(r.message) &&
      r.message.name === t.name &&
      r.message.definition === t.definition,
  });
}

export function termDelete() {
  const list = termList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  client.connect("host.docker.internal:50051", { plaintext: true });
  const result = client.invoke("/term.v1.TermService/Delete", { id: term.id });
  check(result, {
    "is status OK": (r) => r.status === StatusOK,
  });
}

export function termEdit() {
  const list = termList();
  if (list.length === 0) return;
  const term = randomArrayItem(list);
  client.connect("host.docker.internal:50051", { plaintext: true });
  const result = client.invoke("/term.v1.TermService/Update", {
    id: term.id,
    name: term.name,
    definition: uuid(),
  });
  check(result, {
    "is status OK": (r) => r.status === StatusOK,
  });
}

export default termFind;
