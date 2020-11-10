<template>
  <div class="hello">
    <p>The data below is added/removed from the SQLite Database using Django's ORM and Rest Framework.</p>
    <br/>
    <p>Subject</p>
    <input type="text" placeholder="Hello" v-model="subject">
    <p>Message</p>
    <input type="text" placeholder="From the other side" v-model="msgBody">
    <br><br>
    <input 
      type="submit" 
      value="Add" 
      @click="addPost({ subject: subject, body: msgBody })" 
      :disabled="!subject || !msgBody">

    <hr/>
    <h3>Posts on Database</h3>
    <p v-if="posts.length === 0">No Posts</p>
    <div class="msg" v-for="(msg, index) in posts" :key="index">
        <p class="msg-index">[{{index}}]</p>
        <p class="msg-subject" v-html="msg.subject"></p>
        <p class="msg-body" v-html="msg.body"></p>
        <input type="submit" @click="deletePost(msg.pk)" value="Delete" />
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: "Posts",
  data() {
    return {
      subject: "",
      msgBody: "",
    };
  },
  computed: mapState({
    posts: state => state.posts.posts
  }),
  methods: mapActions('posts', [
    'addPost',
    'deletePost'
  ]),
  created() {
    this.$store.dispatch('posts/getPosts')
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
hr {
  max-width: 65%;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

</style>
