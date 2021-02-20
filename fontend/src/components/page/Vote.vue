<template>
	<div>
		<!-- <button v-print="'#printTest'">打印</button> -->
		<!-- <el-button class="button" icon="el-icon-printer" v-print="'#printVote'">打印</el-button> -->
		<div id="printVote" class="print-vote">
<!--			<ul id="uvote">　-->
<!--				<li style="page-break-after:always" v-for="(row,index) in checkedData" :key="index">-->
					<p class="title1">佛山电器照明股份有限公司</p>
					<p class="title2">{{query.year+query.name}}议案表决票</p>
					<table class="table2">
						<tr>
							<th rowspan="2">股东姓名</th>
							<th rowspan="2">股东代码</th>
							<th colspan="2">
								股票种类即持股数
							</th>

						</tr>
						<tr>
							<th>A股</th>
							<th>B股</th>
						</tr>

						<tr>
							<td>{{row.gdxm}}</td>
							<td><barcode v-bind:value="row.gddmk"></barcode></td>
							<td>{{row.gzA}}</td>
							<td>{{row.gzB}}</td>

						</tr>
					</table>
					<br>
      <p v-if="descr">{{descr}}</p>
					<p class="text" v-else>说明：每项议案均有一张表决票，请使用“✓”符号在反对或弃权栏中选择其中一项投出表决票，多选无效。</p>
					<table class="table3">
						<tr >
							<th width="60">议案编号</th>
							<th>议案主题</th>
<!--							<th>赞成</th>-->
							<th>反对</th>
							<th>弃权</th>
						</tr>
						<tr v-for="(m,index) in motion" :key="index" >
							<td>{{index+1}}</td>
							<td>{{m}}</td>
<!--							<td></td>-->
							<td></td>
							<td></td>
						</tr>
					</table>
<!--					<p align="right" class="bottom-p">投票人签名：_____________</p>-->
<!--					<p align="right" class="bottom-p">{{currentDate}}</p>-->
      <br>
      <br>
      <table class="table3">
        <tr >
          <th width="60">议案编号</th>
          <th>议案主题</th>
          <th>赞成</th>
        </tr>
        <tr v-for="(m,index) in leijimotion" :key="index" >
          <td>{{index+1}}</td>
          <td>{{m}}</td>
          <td></td>
        </tr>
      </table>
      <p align="right" class="bottom-p">投票人签名：_____________</p>
      <p align="right" class="bottom-p">{{currentDate}}</p>

<!--				</li>-->
<!--			</ul>-->
		</div>
<!--		<el-pagination layout="prev, pager, next" background @current-change="current_change" :total="10*checkedData.length">-->
<!--		</el-pagination>-->

	</div>
</template>

<script>
import VueBarcode from 'vue-barcode'
export default {
  name: 'vote',
  props: ['query', 'row', 'motion', 'leijimotion', 'descr'],
  components: {
    'barcode': VueBarcode
  },
  data () {
    return {
      BarcodeValue: '',
      currentDate: this.dateToString(),
      datas: ['a', 'b']
    }
  },
  created () {

  },
  methods: {
    dateToString () {
      var _date = new Date()
      var year = _date.getFullYear()
      var month = _date.getMonth() + 1
      var day = _date.getDate()
      var currentDate = year.toString() + '-' + month.toString() + '-' + day.toString()
      return currentDate
    },
    current_change: function (currentPage) {
      // this.currentPage = currentPage;
      var oUl = document.getElementById('uvote')
      console.log(currentPage)
      oUl.style.top = -800 * (currentPage - 1) + 'px'
    }
  }
}
</script>

<style>
	@media screen {
		.print-vote {
			padding-left: 100px;
			padding-right: 100px;
			overflow-y: hidden;
			height: 800px;
			position: relative;



		}

		.print-vote ul {
			list-style-type: none;
			position: absolute;
			left:0px;
			width: 100%;
		}
		
		.print-vote ul li{
			height: 800px;
		}




	}

	@media print {

	}


</style>
