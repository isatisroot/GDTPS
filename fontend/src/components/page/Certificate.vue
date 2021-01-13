<template>
	<div>
		<!-- <div>
			<h3 class="titile3" align="center">佛山电器照明股份有限公司</h3>
			<h2 class="title2" align="center">{{year+name}}登记凭证</h2>
			<p style="text-indent:50px;">此据为参加{{year+name}}现场会议登记凭证，请凭此据于{{date}}到本公司办公楼五楼会议室（佛山市禅城区汾江北路64号），领取会议材料，并参加股东大会。</p>
			<table border="1" style="width: 100%;margin:auto;text-align: center;">
				<tr>
					<th rowspan="2">登记日期</th>
					<th rowspan="2">序号</th>
					<th rowspan="2">股东姓名(单位)</th>
					<th rowspan="2">股东代码</th>
					<th colspan="3">股数数</th>
				</tr>
				<tr>
					<th>A股</th>
					<th>B股</th>
					<th>小计</th>
				</tr>

				<tr>
					<td>{{currentDate}}</td>
					<td>{{currentPage}}</td>
					<td>{{checkedData[currentPage-1].gdxm}}</td>
					<td>{{checkedData[currentPage-1].gddmk}}</td>
					<td>{{checkedData[currentPage-1].gzA}}</td>
					<td>{{checkedData[currentPage-1].gzB}}</td>
					<td>{{checkedData[currentPage-1].gzA + checkedData[0].gzB}}</td>

				</tr>
			</table>
			<p align="right" class="bottom-p">佛山电器照明股份有限公司</p>
			<p align="right" class="bottom-p">{{currentDate}}</p>
		</div>
		<el-pagination layout="prev, pager, next" @current-change="current_change" :total="1000">
		</el-pagination>
 -->
		<!-- <el-button class="button" icon="el-icon-printer"  v-print="'#printCerificate'">打印</el-button> -->
		<div id="printCerificate" class="print-cerificate">
			<ul id="t1">
				<li style="page-break-after:always " v-for="(row,index) in checkedData" :key="index">
					<p class="title1" >佛山电器照明股份有限公司</p>
					<p class="title2">{{year+name}}登记凭证</p>
					<p class="text">此据为参加{{year+name}}现场会议登记凭证，请凭此据于{{date}}到本公司办公楼五楼会议室（佛山市禅城区汾江北路64号），领取会议材料，并参加股东大会。</p>
					<table border="1" class="table1" >
						<tr>
							<th rowspan="2">登记日期</th>
							<th rowspan="2">序号</th>
							<th rowspan="2">股东姓名(单位)</th>
							<th rowspan="2">股东代码</th>
							<th colspan="3">股份数</th>
						</tr>
						<tr>
							<th>A股</th>
							<th>B股</th>
							<th>小计</th>
						</tr>

						<tr>
							<td>{{currentDate}}</td>
							<td>{{index+1}}</td>
							<td>{{row.gdxm}}</td>
							<td>{{row.gddmk}}</td>
							<td>{{row.gzA}}</td>
							<td>{{row.gzB}}</td>
							<td>{{row.gzA + row.gzB}}</td>

						</tr>
					</table>
					<p align="right" class="bottom-p">佛山电器照明股份有限公司</p>
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
		name: 'certificate',
		props: ['year', 'name', 'date', 'checkedData'],
		data() {
			return {
				currentDate: this.dateToString(),
				sumShare: this.Share(),
				currentPage: 1,
				pagesize: 1,
			}
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

			Share() {
				// console.log(this.content)
			},

			getSummaries(param) {
				console.log(param)
			},

			current_change: function(currentPage) {
				// this.currentPage = currentPage;
				var oUl = document.getElementById('t1');
				console.log(currentPage)
				oUl.style.top = -455*(currentPage-1) + 'px'

			},
		}
	}
</script>

<style>
	/* 屏显使用一套CSS，打印使用另一套CSS，解决因为使用overflow无法分页打印的问题 */
	@media screen {
		 .print-cerificate {
			padding-left: 100px;
			padding-right: 100px;
			overflow-y: hidden;
			height: 455px;
			position: relative;

			
		}
		.print-cerificate ul {

			list-style-type: none;
			position: absolute;
		}
		
	
		
		
	}

	@media print {
		.print-cerificate {
			padding-left: 100px;
			padding-right: 100px;


		}
		.print-cerificate ul{
			list-style-type: none;
		}
	}

	/* .printcss {
		padding-left: 100px;
		padding-right: 100px;
	} */
	.bottom-p {
		/* margin-top: 30px; */
		line-height: 55px;
		font-size: 18px;
		
	}
	
	.text{
		text-indent:50px;
		font-size: 20px;
		/* margin-bottom: 10px; */
		line-height: 35px;
	}
	
	.table1{
		width: 100% ;
		margin:auto;
		text-align: center;
		border-collapse:collapse;
		
	}
	.table1 tr th{
		font-family: SimSun;
		font-weight: 900;
		height: 50px;
		font-size: 20px;
		border:1px solid #000000;
	}
	.table1 tr td{
		font-family: times new roman;
		font-weight: 200;
		font-size: 18px;
		border:1px solid #000000;
		height: 50px;
	}
</style>
