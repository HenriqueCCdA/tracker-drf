import http from "@/http";
import {IProjeto, IProjetoApi} from "@/interfaces/IProjeto";
import { Estado } from "@/store";
import { ALTERAR_PROJETO, CADASTRAR_PROJETO, OBTER_PROJETOS, REMOVER_PROJETO } from "@/store/tipo-acoes";
import { ADICIONA_PROJETO, ALTERA_PROJETO, DEFINIR_PROJETOS, EXCLUIR_PROJETO } from "@/store/tipo-mutacoes";
import { Module } from "vuex";

export interface EstadoProjeto{
    projetos: IProjeto[]
}

export const projeto: Module<EstadoProjeto, Estado> =  {
    mutations: {
        [ADICIONA_PROJETO](state, nomeDoProjeto: string) {
            const projeto = {
                id: new Date().toISOString(),
                nome: nomeDoProjeto
            } as IProjeto
            state.projetos.push(projeto)
        },
        [ALTERA_PROJETO](state, projeto: IProjeto) {
            const index = state.projetos.findIndex(proj => proj.id == projeto.id)
            state.projetos[index] = projeto
        },
        [EXCLUIR_PROJETO](state, id: string) {
            state.projetos = state.projetos.filter(proj => proj.id != id)
        },
        [DEFINIR_PROJETOS](state, projetos: IProjetoApi[]) {
            const projeto_lista: IProjeto[] = []
            for(const p of projetos){
                projeto_lista.push({"id": p.id, "nome": p.name})
            }
            state.projetos = projeto_lista
        },
    },
    actions: {
        [OBTER_PROJETOS] ({ commit }) {
            http.get('/project/')
                .then(resposta => commit(DEFINIR_PROJETOS, resposta.data.results))
        },
        [CADASTRAR_PROJETO] (context, nomeDoProjeto: string) {
            return http.post('/project/', {
                name: nomeDoProjeto
            })
        },
        [ALTERAR_PROJETO] (context, projeto: IProjeto) {
            return http.put(`/project/${projeto.id}/`, {"name": projeto.nome})
        },
        [REMOVER_PROJETO] ({commit}, id: string) {
            return http.delete(`/project/${id}`)
                .then(() => commit(EXCLUIR_PROJETO, id))
        },
    }
}
