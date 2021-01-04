<template>
	<div id="printCerificate" class="printcss">
		
	<!-- <el-button type="success" icon="el-icon-printer" @click="printVoucher">打印凭证</el-button> -->
	<!-- <div id="wrap" class="wrap">
		<h3 class="title3" align="center">佛山电器照明股份有限公司</h3>
		<h2 class="title2" align="center">{{year+name}}登记凭证</h2>
		<p align="center">此据为参加{{year+name}}现场会议登记凭证，请凭此据于{{date}}到本公司办公楼五楼会议室（佛山市禅城区汾江北路64号），领取会议材料，并参加股东大会。</p>
		
		<el-table :data="content" border align="center" :summary-method="getSummaries">
			<el-table-column label="登记日期" width="100" align="center">
				<template slot-scope="scope">
					<span>{{currentDate}}</span>
				</template>
			</el-table-column>
			<el-table-column type="index" label="序号" align="center">
			</el-table-column>
			<el-table-column prop="gdxm" label="股东姓名(单位)" width="180" align="center">
			</el-table-column>
			<el-table-column prop="gddmk" label="股东代码" width="110" align="center">
			</el-table-column>
			<el-table-column label="股份数" align="center">
				<el-table-column prop="gzA" label="A股" align="center">
				</el-table-column>
				<el-table-column prop="gzB" label="B股" align="center">
				</el-table-column>
				<el-table-column label="小计" align="center">
					<template slot-scope="scope">
						<span>{{sumShare}}</span>
					</template>
				</el-table-column>
			</el-table-column>

		</el-table>
		
	</div> -->
	<div style="page-break-after:always " v-for="(row,index) in checkedData" :key="row.gdxm">
		<h3 class="titile3" align="center" >佛山电器照明股份有限公司</h3>
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
	</div>
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
				console.log(this.content)
			},
			getSummaries(param) {
				console.log(param)
			},
		}
	}
</script>

<style>
	.printcss {
		padding-left: 100px;
		padding-right: 100px;
	}
	.bottom-p{
		margin: 30px;
	}
</style>
