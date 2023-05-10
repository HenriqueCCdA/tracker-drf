import http from "@/http";
import { ITarefa, ITarefaApi} from "@/interfaces/ITarefa";
import { Estado } from "@/store";
import { ALTERAR_TAREFA, CADASTRAR_TAREFA, OBTER_TAREFAS } from "@/store/tipo-acoes";
import { ADICIONA_TAREFA, ALTERA_TAREFA, DEFINIR_TAREFAS } from "@/store/tipo-mutacoes";
import { Module } from "vuex";

export interface EstadoTarefa{
    tarefas: ITarefa[]
}

export const tarefa: Module<EstadoTarefa, Estado> =  {
    state: {
        tarefas: [],
    },
    mutations: {
        [DEFINIR_TAREFAS](state, tarefas: ITarefaApi[]) {
            const tarefa_lista: ITarefa[] = []
            for(const t of tarefas){
                tarefa_lista.push({
                    "id": t.id,
                    "duracaoEmSegundos": t.duration,
                    "projeto": {"id": "1", "nome": t.project},
                    "descricao": t.description,
                })
            }
            state.tarefas = tarefa_lista
        },
        [ADICIONA_TAREFA](state, tarefa: ITarefa) {
            state.tarefas.push(tarefa)
        },
        [ALTERA_TAREFA](state, tareda: ITarefa) {
            const index = state.tarefas.findIndex(t => t.id == tareda.id)
            state.tarefas[index] = tareda
        },
    },
    actions: {
        [OBTER_TAREFAS] ({ commit }, filtro: string) {
            let url = '/task/';
            if (filtro) {
                url += '?descricao=' + filtro
            }
            http.get(url)
                .then(resposta => commit(DEFINIR_TAREFAS, resposta.data.results))
        },
        [CADASTRAR_TAREFA] ({commit}, tarefa: ITarefa) {
            return http.post('/tarefas', tarefa)
                .then(resposta => commit(ADICIONA_TAREFA, resposta.data))
        },
        [ALTERAR_TAREFA] ({ commit }, tarefa: ITarefa) {
            return http.put(`/tarefas/${tarefa.id}`, tarefa)
                .then(() => commit(ALTERA_TAREFA, tarefa))
        },
    }
}
