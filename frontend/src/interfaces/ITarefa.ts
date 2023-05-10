import {IProjeto} from "./IProjeto";

export interface ITarefa {
  duracaoEmSegundos: number,
  descricao: string,
  projeto: IProjeto,
  id: number
}

export interface ITarefaApi {
  description: string,
  duration: number,
  project:  string,
  id: number
}
