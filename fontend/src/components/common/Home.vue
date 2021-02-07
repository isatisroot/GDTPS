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
