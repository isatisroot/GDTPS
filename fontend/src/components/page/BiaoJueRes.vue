<template>
  <div id="res1">
    <p class="title1" >佛山电器照明股份有限公司</p>
    <p  class="title2" align="center">{{query.year+query.name}}议案投票表决统计结果</p>
    <h4>一、会议的出席情况</h4>
    <h5>1.出席的总体情况：</h5>
    <p>{{content.content1}}</p>
    <h5>2.A股股东出席情况：</h5>
    <p>{{content.content2}}</p>
    <h5>3.B股股东出席情况：</h5>
    <p>{{content.content3}}</p>
    <h5>4.中小股出席情况：</h5>
    <p>{{content.content4}}</p>
    <el-divider></el-divider>
    <template v-for="con in content.content5">
      <li>{{con.name}}</li>
      <p>{{con.content}}</p>
      <el-divider></el-divider>
    </template>
    <template v-for="con in content.content6">
      <li>{{con.name}}</li>
      <p>{{con.content}}</p>
      <el-divider></el-divider>
    </template>
  </div>
</template>

<script>
export default {
  name: 'BiaoJueRes',
  data () {
    return{
      query: {
        year: '',
        name: ''
      }
    }
  },
  props: ['content'],
  created () {
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
  },
  mounted () {

  },
  updated () {
    // 当有更新时重新读取
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
  }
}
</script>

<style scoped>
p{ text-indent:2em;}
</style>