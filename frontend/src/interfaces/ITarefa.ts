import {IProjeto} from "./IProjeto";

export interface ITarefa {
  id: string,
  duracaoEmSegundos: number,
  descricao: string,
  projeto: IProjeto,
}

export interface ITarefaApi {
  id: string,
  description: string,
  duration: number,
  project_id: string,
  project_name: string,
}
