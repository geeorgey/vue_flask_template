<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar text dense flat>
            <v-toolbar-title> ToDo登録 </v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-divider />
          <v-card-text>
            <v-text-field
              v-model="formModel.todo"
              outlined
              label="ToDo"
              placeholder="ToDoを入力"
              :append-icon="'mdi-location'"
              required
            />
          </v-card-text>
          <v-divider class="mt-5"></v-divider>
          <v-card-actions>
            <v-spacer />
            <v-btn tile color="accent" @click="handleSubmitForm">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card tile>
          <v-card-title>登録済みToDo</v-card-title>
          <v-divider />
          <v-data-table
            v-model="selected"
            show-select
            :headers="todo_headers"
            :items="$store.state.todo.todos"
            hide-default-footer
            class="elevation-0 table-striped"
          >
          </v-data-table>
          <v-divider class="mt-5"></v-divider>
          <v-card-actions>
            <v-spacer />
            <v-btn tile color="error" @click="handleDeleteToDos"> 削除する </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TooltipMixin from '@/mixins/Tooltip'
import { mapGetters } from 'vuex'
export default {
  mixins: [TooltipMixin],
  data() {
    return {
      loadingItems: false,
      selectedItem: null,
      serverItemsLength: 0,
      itemsPerPage: 15,
      filter: {
        page: 1,
        'filter[name]': null,
        'filter[project_id]': null,
        'filter[status]': null,
      },
      todo_headers: [
        {
          text: 'ToDo',
          value: 'name',
        },
      ],
      items: [],
      formModel: {
        todo: null,
      },
      selected: [],
    }
  },
  computed: {
    ...mapGetters(['getToDos']),
  },
  mounted() {
    this.$store
      .dispatch('fetchTodo', {
        user_id: this.$store.state.auth.user_id,
      })
      .then(() => {
        //console.log('getToDos-----')
        //console.log(getToDos)
      })
      .catch(() => {
        this.loading = false
      })
  },
  methods: {
    handleSubmitForm() {
      console.log('handleSubmitForm')
      console.log(this.formModel)
      console.log('todo: ' + this.formModel.todo)
      this.loading = true
      if (this.formModel.todo != null) {
        this.$store
          .dispatch('addtodo', { todo: this.formModel.todo, user_id: this.$store.state.auth.user_id })
          .then(() => {
            this.loading = false
          })
          .catch(() => {
            this.loading = false
          })
      }
    },
    handleDeleteToDos(){
      console.log('handleDeleteToDos')
      //console.log(this.selected_message)
      if (this.selected.length > 0) {
        console.log('selected')
        console.log(this.selected)
        this.$store
          .dispatch('deleteToDo', {
            delete_todos: this.selected,
            user_id: this.$store.state.auth.user_id,
          })
          .then(() => {
            this.loading = false
          })
          .catch(() => {
            this.loading = false
          })
      }
    }
  },
}
</script>
