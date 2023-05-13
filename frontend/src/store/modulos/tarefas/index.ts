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
                console.log(t)
                tarefa_lista.push({
                    "id": t.id,
                    "duracaoEmSegundos": t.duration,
                    "projeto": {"id": t.project_id, "nome": t.project_name},
                    "descricao": t.description,
                })
            }
            console.log(tarefa_lista)
            state.tarefas = tarefa_lista
        },
        [ADICIONA_TAREFA](state, tarefa: ITarefaApi) {

            const tarefa_nova: ITarefa = {
                "id": tarefa.id,
                "duracaoEmSegundos": tarefa.duration,
                "projeto": {"id": tarefa.project_id, "nome": tarefa.project_name},
                "descricao": tarefa.description,
            }

            state.tarefas.push(tarefa_nova)
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
                url += '?description=' + filtro
            }
            http.get(url)
                .then(resposta => commit(DEFINIR_TAREFAS, resposta.data.results))
        },
        [CADASTRAR_TAREFA] ({commit}, tarefa: ITarefa) {

            const payload = {
                "description": tarefa.descricao,
                "duration": tarefa.duracaoEmSegundos,
                "project": tarefa.projeto.id,
            }
            return http.post('/task/', payload)
                .then(resposta => commit(ADICIONA_TAREFA, resposta.data))
        },
        [ALTERAR_TAREFA] ({ commit }, tarefa: ITarefa) {

            const payload = {
                "description": tarefa.descricao,
                "duration": tarefa.duracaoEmSegundos,
                "project": tarefa.projeto.id,
            }

            return http.put(`/task/${tarefa.id}/`, payload)
                .then(() => commit(ALTERA_TAREFA, tarefa))
        },
    }
}
