<template>
  <div id="Article">
    <div class="inner-top"></div>
    <div class="inner-bottom">
        
    </div>
  </div>
</template>

<script>
export default {
  name: 'Article',
  data() {
      return {
          
      }
  },
  computed: {
    
  },
  methods: {
    
  },
  mounted() {

  }
}
</script>

<style scoped>

#Article {
    position: relative;
    background-color:aqua;
    height: 100%;
}

.inner-top {
    position: absolute;
    top: 10px;
    left: 20px;
    right: 20px;
    height: 60px;
}

.inner-bottom {
    position: absolute;
    background-color: #fff;
    top: 100px;
    bottom: 20px;
    left: 20px;
    right: 20px;
    box-shadow: 0px 0px 2px 3px #e5e5e5;
    border-radius: 5px;
    overflow: auto;
}

</style>
