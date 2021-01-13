<template>
	<div>
		<!-- <button v-print="'#printTest'">打印</button> -->
		<!-- <el-button class="button" icon="el-icon-printer" v-print="'#printVote'">打印</el-button> -->
		<div id="printVote" class="print-vote">
			<ul id="uvote">　
				<li style="page-break-after:always" v-for="(row,index) in checkedData" :key="index">
					<p class="title1">佛山电器照明股份有限公司</p>
					<p class="title2">{{year+name}}议案表决票</p>
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
							<td>{{row.gddmk}}</td>
							<td>{{row.gzA}}</td>
							<td>{{row.gzB}}</td>
						</tr>
					</table>
					<br>
					<p class="text">说明：每项议案均有一张表决票，请使用“✓”符号在赞成、反对或弃权栏中选择其中一项投出表决票，多选无效。</p>
					<table class="table3">
						<tr>
							<th>议案编号</th>
							<th>议案主题</th>
							<th>赞成</th>
							<th>反对</th>
							<th>弃权</th>
						</tr>
						<tr v-for="(m,index) in motion" :key="index">
							<td>{{index+1}}</td>
							<td>{{m}}</td>
							<td></td>
							<td></td>
							<td></td>
						</tr>
					</table>
					<p align="right" class="bottom-p">投票人签名：_____________</p>
					<p align="right" class="bottom-p">{{currentDate}}</p>

				</li>
			</ul>
		</div>
		<el-pagination layout="prev, pager, next" background @current-change="current_change" :total="10*checkedData.length">
		</el-pagination>

	</div>
</template>

<script>
	export default {
		name: 'vote',
		props: ['year', 'name', 'checkedData', 'motion'],
		data() {
			return {
				currentDate: this.dateToString(),
				datas: ['a', 'b']
			}
		},
		created() {

		},
		methods: {
			dateToString() {
				var _date = new Date();
				var year = _date.getFullYear();
				var month = _date.getMonth() + 1;
				var day = _date.getDate();
				var currentDate = year.toString() + '-' + month.toString() + '-' + day.toString();
				return currentDate
			},
			current_change: function(currentPage) {
				// this.currentPage = currentPage;
				var oUl = document.getElementById('uvote');
				console.log(currentPage)
				oUl.style.top = -592 * (currentPage - 1) + 'px'

			},
		},
	}
</script>

<style>
	@media screen {
		.print-vote {
			padding-left: 100px;
			padding-right: 100px;
			overflow-y: hidden;
			height: 592px;
			position: relative;



		}

		.print-vote ul {
			list-style-type: none;
			position: absolute;
		}




	}

	@media print {
		.print-cerificate {
			padding-left: 100px;
			padding-right: 100px;


		}

		.print-cerificate ul {
			list-style-type: none;
		}
	}

	.table2,
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
</style>
