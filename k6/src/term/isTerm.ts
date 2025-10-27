import { Term } from "./types";

export function isTerm(obj: unknown): obj is Term {
  return (
    typeof obj === "object" &&
    obj !== null &&
    "id" in obj &&
    "name" in obj &&
    "definition" in obj
  );
}
