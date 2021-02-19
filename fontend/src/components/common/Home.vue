<template>
    <div class="wrapper">
        <v-head></v-head>
        <v-sidebar></v-sidebar>
        <div class="content-box" :class="{'content-collapse':collapse}">
            <v-tags></v-tags>
            <div class="content">
                <transition name="move" mode="out-in">
<!--                  禁用缓存，使子组件中状态更新时，共享的数据在其他组件及时响应-->
<!--                    <keep-alive :include="tagsList">-->
						<!-- 路由出口 -->
						  <!-- 路由匹配到的组件将渲染在这里 -->
                        <router-view></router-view>
<!--                    </keep-alive>-->
                </transition>
                <el-backtop target=".content"></el-backtop>
            </div>
        </div>
    </div>
</template>

<script>
import vHead from './Header.vue'
import vSidebar from './Sidebar.vue'
import vTags from './Tags.vue'
import bus from './bus'
import {EventBus} from '@/api/event_bus'
export default {
  data () {
    return {
      tagsList: [],
      collapse: false,
      year: null,
      name: null
    }
  },
  components: {
    vHead,
    vSidebar,
    vTags
  },
  created () {
    EventBus.$on('addition', param => {
      this.year = param.year
      this.name = param.meetingName
    })
    bus.$on('collapse-content', msg => {
      this.collapse = msg
    })

    // 只有在标签页列表里的页面才使用keep-alive，即关闭标签之后就不保存到内存中了。
    bus.$on('tags', msg => {
      let arr = []
      for (let i = 0, len = msg.length; i < len; i++) {
        msg[i].name && arr.push(msg[i].name)
      }
      this.tagsList = arr
    })
  }
}
</script>
<style>
.page,.page-box{
  margin: 0 auto;
  width: 650px;
  padding: 50px 0 0 60px;
  background: #fff;
  /*background: url("../../assets/img/box-bg.jpg");*/
  border-radius: 20px;
  text-align: justify;
}
.page-box{
  padding: 0 60px 40px 0;
}
.page{
  position: relative;
  /*margin-left: 0;*/

  filter: drop-shadow(0px 0px 15px #bbb);
}
.page:before{
  content: '';
  display: block;
  position: absolute;
  right:-60px;
  top:0;
  width: 60px;
  height: 50px;
  background: linear-gradient(42deg, #ddd 30%, rgba(0,0,0,0) 40%);
}
.button-group {
  /* font-size: 0; */
  /* Inline block elements gap - fix */
  /* margin-bottom: 10px; */
  padding: 0;
  /*background: #E64A19;*/
  background: linear-gradient(to bottom, #FF5722, #FFCCBC);
  /* border-bottom: 1px solid rgba(0, 0, 0, .1); */
  padding: 7px;
  -moz-border-radius: 7px;
  -webkit-border-radius: 7px;
  border-radius: 7px;
  /* float: right; */
}
.title1 {
  /* margin-top: 30px; */
  /* margin-bottom: 10px; */
  text-align: center;
  font-size: 30px;
  font-family: "LiSu";
  color: orangered;

}

.title2 {
  /* margin-top: 15px; */
  /* margin-bottom: 20px; */
  line-height: 80px;
  text-align: center;
  font-size: 28px;
  color: indianred
}

.table1{
  /*width: 100% ;*/
  margin:auto;
  text-align: center;
  border-collapse:collapse;

}
.table1 tr th{
  font-family: SimSun;
  font-weight: 900;
  height: 50px;
  font-size: 18px;
  border:1px solid #000000;
}
.table1 tr td{
  font-family: times new roman;
  font-weight: 200;
  font-size: 14px;
  border:1px solid #000000;
  height: 50px;
}

.table2{
  width:70%;
  margin: auto;
  text-align: center;
  border-collapse: collapse;
}

.table3 {
  width: 100%;
  margin: auto;
  text-align: center;
  border-collapse: collapse;
}

.table2 tr th,
.table3 tr th {
  font-family: SimSun;
  font-weight: 900;
  height: 50px;
  font-size: 20px;
  border: 1px solid #000000;
}

.table2 tr td,
.table3 tr td {
  font-family: STSong;
  font-weight: 200;
  font-size: 18px;
  border: 1px solid #000000;
  height: 50px;
}

.table4 {
  width: 100%;
  margin: auto;
  text-align: center;
  border-collapse: collapse;
}


.table4 tr th {
  font-family: SimSun;
  font-weight: 900;
  height: 50px;
  font-size: 18px;
  border: 1px solid #000000;
}


.table4 tr td {
  font-family: times new roman;
  font-weight: 200;
  font-size: 14px;
  border: 1px solid #000000;
  height: 50px;
}
</style>
