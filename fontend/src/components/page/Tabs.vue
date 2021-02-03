<template>
	<div >
		<!-- <div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-lx-copy"></i> 股东信息</el-breadcrumb-item>
			</el-breadcrumb>
		</div> -->
    <ul class="button-group">
      <div class="button-group-left">
<!--        <el-button class="button" icon="el-icon-circle-plus" @click="addRow">增加</el-button>-->
<!--        <el-button class="button" icon="el-icon-delete" @click="handleDelete(row.index,row)" >删除</el-button>-->
        <el-button class="button" icon="el-icon-printer" @click="">统计表</el-button>
        <el-button class="button" icon="el-icon-printer" @click="" v-print="'#res1'">表决结果</el-button>
        <el-button class="button" icon="el-icon-success" @click="">保存</el-button>
      </div>
    </ul>
		<div class="container">
      <el-tabs v-model="message" type="border-card" >
        <el-tab-pane name="first" >
        <p class="title1" >佛山电器照明股份有限公司</p>
        <p  class="title2" align="center">{{query.year+query.name}}议案表决投反对票、弃权票统计表</p>
        <table class="table4" id="yianTable">
          <tr>
            <th rowspan="2" width="40">议案编号</th>
            <th rowspan="2" width="25">子编号</th>
            <th rowspan="2" width="300">议案主题</th>
            <th colspan="4" width="300">反对票</th>
            <th colspan="4" width="300">弃权票</th>
            <th rowspan="2" width="40">采用累积投票</th>
            <th rowspan="2" width="40">存在回避票</th>
            <th colspan="2" width="280">回避票数</th>
            <th rowspan="2" width="150">回避表述</th>
          </tr>
          <tr>
            <th colspan="2">股份数</th>
            <th>小计</th>
            <th>合计</th>
            <th colspan="2">股份数</th>
            <th>小计</th>
            <th>合计</th>
            <th>A股</th>
            <th>B股</th>
          </tr>
  <!--        <li  v-for="(m,index) in motion" :key="index">-->
          <tbody v-for="(m,index) in motion" :key="index" class="tbody-input">
  <!--        <tbody>-->
          <tr >
            <td rowspan="2" >1</td>
            <td rowspan="2" >1</td>
            <td rowspan="2" >{{m}}</td>
            <td>A股</td>
            <td><input class="border-input" v-model.number="array1[index]" @keyup.enter="fun1(array1[index], index)"></input></td>
            <td width="80">{{countFanA[index].count}}</td>
            <td rowspan="2" width="80">{{countFanA[index].count + countFanB[index].count}}</td>
            <td>A股</td>
            <td><input v-model.number="array2[index]" @keyup.enter="fun2(array2[index], index)"></input></td>
            <td width="80">{{countQiA[index].count}}</td>
            <td rowspan="2" width="80">{{countQiB[index].count + countQiB[index].count}}</td>
            <td rowspan="2"></td>
            <td rowspan="2"></td>
            <td rowspan="2" ><input></input></td>
            <td rowspan="2"><input></input></td>
            <td rowspan="2"></td>
          </tr>
          <tr>
            <!--          <td colspan="0"></td>-->
            <!--          <td rowspan="0"></td>-->
            <!--          <td rowspan="0"></td>-->
            <td>B股</td>
            <td><input class="border-input" v-model.number="array3[index]" @keyup.enter="func3(array3[index], index)"></input></td>
            <td>{{countFanB[index].count}}</td>
            <!--          <td rowspan="2"></td>-->
            <td>B股</td>
            <td><input v-model.number="array4[index]" @keyup.enter="func4(array4[index], index)"></input></td>
            <td>{{countQiB[index].count}}</td>
            <!--          <td></td>-->
            <!--          <td></td>-->
            <!--          <td></td>-->
            <!--          <td></td>-->
            <!--          <td></td>-->
            <!--          <td></td>-->
          </tr>
          </tbody>

  <!--        </li>-->


        </table>
        <br>
        </el-tab-pane>
        <el-tab-pane disabled name="second">
              <BiaoJueRes></BiaoJueRes>
        </el-tab-pane>
        <el-tab-pane disabled name="third">
<!--          <Director></Director>-->
        </el-tab-pane>
      </el-tabs>
		</div>

	</div>
</template>


<script>
import {
  EventBus
} from '../../api/event_bus.js'
import BiaoJueRes from './BiaoJueRes'
import Director from "@/components/page/Director";
import axios from "axios";
export default {
  name: 'tabs',
  components: {BiaoJueRes, Director},
  data () {
    return {
      message: 'first',
      array1: [],
      array2: [],
      array3: [],
      array4: [],
      countFanA: [{count: null}, {count: null}, {count: null}],
      countQiA: [{count: null}, {count: null}, {count: null}],
      countFanB: [{count: null}, {count: null}, {count: null}],
      countQiB: [{count: null}, {count: null}, {count: null}],
      sumFan: null,
      sumQi: null,
      query: {
        year: '',
        name: ''
      },
      motion: ['yianyi', 'yianaa']
    }
  },
  created () {
    console.log('created')
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
    axios.get(this.host + 'get_detail/' + this.query.year + '/' + this.query.name).then(response => {
      console.log(response.data)
    }).catch(error => {
      console.log(error)
    })
  },
  mounted () {

  },
  updated () {
  },

  methods: {
    fun1 (v, index) {
      console.log(index)
      this.countFanA[index].count += v
      this.array1[index] = null
      // let dom = document.getElementsByClassName("tbody-input")
      // console.log(dom[index].tr)
      // 敲回车后自动聚焦下一行输入框
      // let nextInput = dom[index + 1]
      // nextInput.focus()
    },
    fun2 (value, index) {
      this.countQiA[index].count += value
      this.array2[index] = null
    },
    func3 (value, index) {
      this.countFanB[index].count += value
      this.array3[index] = null
      // let dom = document.getElementsByClassName("border-input")
      // let currInput = dom[index]
      // let nextInput = dom[index + 2]
      // console.log(nextInput)
      // nextInput.focus()
    },
    func4 (value, index) {
      this.countQiB[index].count += value
      this.array4[index] = null
    }
  }
}
</script>
<style scoped>
 #yianTable input{
   width: 80px;
 }
</style>
