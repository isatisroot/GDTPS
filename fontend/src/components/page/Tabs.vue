<template>
	<div class="">
		<!-- <div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-lx-copy"></i> 股东信息</el-breadcrumb-item>
			</el-breadcrumb>
		</div> -->
		<div class="container">
      <p class="title1" >佛山电器照明股份有限公司</p>
      <p  class="title2" align="center">{{query.year+query.name}}议案表决投反对票、弃权票统计表</p>
      <table class="table4">
        <tr>
          <th rowspan="2" width="40">议案编号</th>
          <th rowspan="2" width="25">子编号</th>
          <th rowspan="2" width="300">议案主题</th>
          <th colspan="4" width="300">反对票</th>
          <th colspan="4" width="300">弃权</th>
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
        <tbody v-for="(m,index) in motion" :key="index">
        <tr >
          <td rowspan="2" >1</td>
          <td rowspan="2" >1</td>
          <td rowspan="2" >\{{m}}</td>
          <td>A股</td>
          <td>输入A股数</td>
          <td>显示A股小计</td>
          <td rowspan="2">合计数</td>
          <td>A股</td>
          <td>输入A股数</td>
          <td>显示小计</td>
          <td rowspan="2">合计数</td>
          <td rowspan="2"></td>
          <td rowspan="2"></td>
          <td rowspan="2"></td>
          <td rowspan="2"></td>
          <td rowspan="2"></td>
        </tr>
        <tr>
          <!--          <td colspan="0"></td>-->
          <!--          <td rowspan="0"></td>-->
          <!--          <td rowspan="0"></td>-->
          <td>B股</td>
          <td>输入B股数</td>
          <td>显示小计数</td>
          <!--          <td rowspan="2"></td>-->
          <td>B股</td>
          <td>输入B股数</td>
          <td>显示小计数</td>
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
		</div>
	</div>
</template>


<script>
import {
  EventBus
} from '../../api/event_bus.js'
export default {
  name: 'tabs',
  data () {
    return {
      query: {
        year: ''
      },
      motion: []
    }
  },
  created() {
    EventBus.$on('baseform', param => {
      this.query = param.query
      this.motion = param.motion

    })
  }
}
</script>
<style>
</style>
