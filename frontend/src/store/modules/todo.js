import request from '@/util/request'

const state = {
  todos: []
}

// getters
const getters = {
  getToDos: (state) => state.todos,
}

// actions
const actions = {
  addtodo({ commit }, { todo, user_id }) {
    return request({
      url: '/addtodo',
      method: 'post',
      data: {
        todo,
        user_id,
      },
    }).then((resp) => {
      console.log('After addtodo')
      console.log(resp)
      commit('SET_TODO', { todos: resp.todo_list })
      //dispatch('fetchGoogleMembers',email)
    })
  },
  deleteToDo({ commit }, { delete_todos, user_id }) {
    return request({
      url: '/deleteToDo',
      method: 'post',
      data: {
        delete_todos,
        user_id,
      },
    }).then((resp) => {
      console.log('After deleteToDo')
      console.log(resp)
      commit('SET_TODO', { todos: resp.todo_list })
      //dispatch('fetchGoogleMembers',email)
    })
  },
  fetchTodo({ commit }, { user_id }) {
    return request({
      url: '/fetchTodo',
      method: 'post',
      data: {
        user_id,
      },
    }).then((resp) => {
      console.log('After addtodo')
      console.log(resp)
      commit('SET_TODO', { todos: resp.todo_list })
      //dispatch('fetchGoogleMembers',email)
    })
  },
}

// mutations
const mutations = {
  SET_PROJECT(state, data) {
    state.projects = data
  },
  SET_TODO(state, payload) {
    console.log('SET_TODO')
    console.log(payload)
    state.todos = payload.todos
    console.log('state.todos')
    console.log(state.todos)
  },
}

export default {
  namespace: true,
  state,
  getters,
  actions,
  mutations,
}
