export interface ID {
  id: number;
}

export interface TermPost {
  name: string;
  definition: string;
}

export interface Term extends TermPost, ID {}
