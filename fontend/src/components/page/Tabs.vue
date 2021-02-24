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
        <el-button class="button" icon="el-icon-printer" @click="printRes1">统计表</el-button>
        <el-button class="button" icon="el-icon-printer" @click="" v-print="'#res1'">表决结果</el-button>
        <el-button class="button" icon="el-icon-download" @click="download">下载</el-button>
      </div>
    </ul>
		<div class="container">
      <el-tabs v-model="message" type="border-card" >
        <el-tab-pane name="first" >
          <div id="printRes1">
        <p class="title1" >佛山电器照明股份有限公司</p>
        <p  class="title2" align="center">{{query.year+query.name}}议案表决投反对票、弃权票统计表</p>
        <table class="table4" id="yianTable">
          <tr>
            <th rowspan="2" width="40">议案编号</th>
            <th rowspan="2" width="25">子编号</th>
            <th rowspan="2" width="300">议案主题</th>
            <th colspan="3" width="300">反对票</th>
            <th colspan="3" width="300">弃权票</th>

            <th rowspan="2" width="40">存在回避票</th>
            <th colspan="2" width="200">回避票数</th>
            <th rowspan="2" width="150">回避表述</th>
          </tr>
          <tr>
            <th >A股</th>
            <th>B股</th>
            <th>合计</th>
            <th >A股</th>
            <th>B股</th>
            <th>合计</th>
            <th>A股</th>
            <th>B股</th>
          </tr>
  <!--        <li  v-for="(m,index) in motion" :key="index">-->
          <tbody v-for="(m,index) in motion" :key="index" class="tbody-input">
  <!--        <tbody>-->
          <tr >
            <td  >{{index + 1}}</td>
            <td  >{{m.id}}</td>
            <td >{{m.name}}</td>
            <td>{{m.fanduiA}}</td>
<!--            <td><input class="border-input" v-model.number="array1[index]" @keyup.enter="fun1(array1[index], index)"></input></td>-->
            <td >{{m.fanduiB}}</td>
            <td >{{m.fanduiA + m.fanduiB}}</td>
            <td>{{m.qiquanA}}</td>
<!--            <td><input v-model.number="array2[index]" @keyup.enter="fun2(array2[index], index)"></input></td>-->
            <td >{{m.qiquanB}}</td>
            <td  >{{m.qiquanA + m.qiquanB}}</td>
            <td v-if="m.is_huibi">✓</td>
            <td v-else></td>
<!--            <td ></td>-->
            <td  >{{m.huibiA}}</td>
            <td >{{m.huibiB}}</td>
            <td >{{m.huibi_descr}}</td>
          </tr>
<!--          <tr>-->
<!--            &lt;!&ndash;          <td colspan="0"></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td rowspan="0"></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td rowspan="0"></td>&ndash;&gt;-->
<!--&lt;!&ndash;            <td>B股</td>&ndash;&gt;-->
<!--            <td><input class="border-input" v-model.number="array3[index]" @keyup.enter="func3(array3[index], index)"></input></td>-->
<!--            <td>{{countFanB[index].count}}</td>-->
<!--            &lt;!&ndash;          <td rowspan="2"></td>&ndash;&gt;-->
<!--&lt;!&ndash;            <td>B股</td>&ndash;&gt;-->
<!--            <td><input v-model.number="array4[index]" @keyup.enter="func4(array4[index], index)"></input></td>-->
<!--            <td>{{countQiB[index].count}}</td>-->
<!--            &lt;!&ndash;          <td></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td></td>&ndash;&gt;-->
<!--            &lt;!&ndash;          <td></td>&ndash;&gt;-->
<!--          </tr>-->
          </tbody>

  <!--        </li>-->


        </table>
        <br>
          <p  class="title2" align="center">{{query.year+query.name}}议案表决董事表决赞成票统计表</p>
          <p>出席会议股东代表股数：{{sharehold_cx_B + sharehold_cx_A}}股，其中B股：{{sharehold_cx_B}}股。</p>
          <table class="table4">
            <tr>
              <th rowspan="2" width="40">议案编号</th>
              <th rowspan="2" width="25">子编号</th>
              <th rowspan="2" width="300">议案主题</th>
              <th colspan="3" width="300">赞成票</th>
            </tr>
            <tr>
              <th >A股</th>
              <th>B股</th>
              <th>合计</th>
            </tr>
            <tr v-for="(m, index) in leijimotion" :key="index">
              <td>{{index+1}}</td>
              <td></td>
              <td>{{m.name}}</td>
              <td>{{m.zanchengA}}</td>
              <td>{{m.zanchengB}}</td>
              <td>{{m.zanchengA + m.zanchengB}}</td>
            </tr>
          </table>
          </div>

          <div class="schart-box">
            <!--                <div class="content-title">柱状图</div>-->
            <schart class="schart" canvasId="bar" :options="options1"></schart>
          </div>
          <div class="schart-box">
            <!--                <div class="content-title">环形图</div>-->
            <schart class="schart" canvasId="ring" :options="options4"></schart>
          </div>
<!--          <div class="schart-box">-->
<!--            &lt;!&ndash;                <div class="content-title">饼状图</div>&ndash;&gt;-->
<!--            <schart class="schart" canvasId="pie" :options="options3"></schart>-->
<!--          </div>-->

        </el-tab-pane>
        <el-tab-pane disabled name="second">
              <BiaoJueRes :content="content" ></BiaoJueRes>
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
import Director from '@/components/page/Director'
import axios from 'axios'
import Schart from 'vue-schart'
import {Print} from "@/utils/Print";
export default {
  name: 'tabs',
  components: {BiaoJueRes, Director, Schart},
  data () {
    return {
      content: null,
      options1: {
        // scales: {
        //
        // },

        leftPadding: 140, // 坐标轴距离左边框距离
        type: 'bar',
        title: {
          text: '各项议案表决情况统计'
        },
        legend: {
          position: 'bottom',
          bottom: 20
        },
        bgColor: '#fbfbfb',
        labels: [],
        datasets: [
          {
            label: '赞成票',
            fillColor: 'rgba(241,49,74,0.5)',
            data: []
          },
          {
            label: '反对票',
            data: []
          },
          {
            label: '弃权票',
            fillColor: 'rgb(49,164,241)',
            data: []
          }
        ]
      },
      options3: {
        type: 'pie',
        title: {
          text: '股东出席情况'
        },
        legend: {
          position: 'left'
        },
        bgColor: '#fbfbfb',
        labels: [],
        datasets: [
          {
            data: []
          }
        ]
      },
      options4: {
        type: 'ring',
        title: {
          text: '累积投票议案表决情况'
        },
        showValue: true,
        legend: {
          position: 'bottom',
          bottom: 40
        },
        bgColor: '#fbfbfb',
        labels: [],
        datasets: [
          {
            data: []
          }
        ]
      },
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
      motion: ['yianyi', 'yianaa'],
      leijimotion: [],
      sharehold_cx_B: 0,
      sharehold_cx_A: 0
    }
  },
  created () {
    console.log('created')
    this.query.year = JSON.parse(localStorage.getItem('year'))
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
    axios.get(this.host + 'result/' + this.query.year + '/' + this.query.name).then(response => {
      console.log(response.data)
      this.motion = response.data['motion']
      this.leijimotion = response.data['leijimotion']
      this.sharehold_cx_A = response.data['sharehold_cx_A']
      this.sharehold_cx_B = response.data['sharehold_cx_B']
      this.content = response.data['content']

      this.options3.labels = response.data['cx_gd']
      this.options3.labels.push('未出席股东')
      this.options3.datasets[0].data = response.data['cx_gb']
      let ncx = response.data['ncx_gb']
      this.options3.datasets[0].data.push(ncx)
      let res1 = response.data['motion']
      let res2 = response.data['leijimotion']
      res1.forEach(item => {
        this.options1.labels.push(item.name)
        this.options1.datasets[0].data.push(item.zanchengA + item.zanchengB)
        this.options1.datasets[1].data.push(item.fanduiA + item.fanduiB)
        this.options1.datasets[2].data.push(item.qiquanA + item.qiquanB)
      })
      res2.forEach(item => {
        this.options4.labels.push(item.name)
        this.options4.datasets[0].data.push(item.zanchengA + item.zanchengB)
      })
    }).catch(error => {
      console.log(error)
    })
  },
  mounted () {

  },
  updated () {
  },

  methods: {
    formatter (val) {
      return val.slice(0, 9)+'' + val.slice(9)
    },
    printRes1 () {
      Print('#printRes1', {
        // 以下class属性的div元素不会打印
        noPrint: '.do-not-print-me',
        onStart: function () {
          console.log('onStart', new Date())
        },
        onEnd: function () {
          console.log('onEnd', new Date())
        }
      })
    },
    download () {
      let url = this.host + 'download_file'
      let data = JSON.stringify({
        file_name: this.query.year + this.query.name,
        year: this.query.year,
        name: this.query.name
      })
      console.log('data:', data)
      axios(
        {
          method: 'post',
          url: url,
          data: data,
          responseType: 'blob' // 指定获取数据的类型为blob
        }
      ).then(
        response => {
          data = response.data // 创建a标签并点击， 即触发下载
          let url = window.URL.createObjectURL(new Blob([data], {type: 'application/msword'})) // application/msword指定下载word类型文件
          let link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          let name = this.query.year + this.query.name
          link.setAttribute('download', name)

          document.body.appendChild(link)
          link.click()
        }
      ).catch(function (err) {
        console.log(err)
      })
    },
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
 .schart-box {
   display: inline-block;
   margin: 20px;
 }
 .schart {
   width: 600px;
   height: 400px;
 }
</style>
