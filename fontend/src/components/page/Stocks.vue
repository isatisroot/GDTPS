<template>
	<div>
		<!-- <el-button class="button" icon="el-icon-printer" v-print="'#printStock'">打印</el-button> -->
	
		<div id="printStock">
		<p class="title1" >佛山电器照明股份有限公司</p>
		<p  class="title2" align="center">{{query.year+query.name}}股东、股份数统计表</p>
		<p class="text">公司总股本：{{share.totalShare}}股，其中A股：{{share.AShareTotal}}股，B股：{{share.BShareTotal}}股</p>
		<table class="table1">
			<tr>
				<th></th>
				<th>股东人数</th>
				<th>代表股份数</th>
				<th>占股份%</th>
				<th>备注</th>
			</tr>
			<tr>
				<td>A股</td>
				<td>{{summary.PeopleA}}</td>
				<td>{{summary.AStock}}</td>
				<td>{{summary.PercentA}}</td>
				<td>占公司A股总数%</td>
			</tr>
			<tr>
				<td>B股</td>
				<td>{{summary.PeopleB}}</td>
				<td>{{summary.BStock}}</td>
				<td>{{summary.PercentB}}</td>
				<td>占公司B股总数%</td>
			</tr>
			<tr>
				<td>合计</td>
				<td>{{summary.PeopleB + summary.PeopleA}}</td>
				<td>{{summary.BStock + summary.AStock}}</td>
				<td>{{summary.PercentTotal}}</td>
				<td>占公司总股本%</td>
			</tr>
		</table>
		<p align="right" class="bottom-p">统计人签字：____________</p>
		<p> 注：统计至开会开始前{{query.date}},请在{{query.date}}前送到主席台</p>
		<p align="right" class="bottom-p">佛山电器照明股份有限公司</p>
		<p align="right" class="bottom-p">{{currentDate}}</p>
	</div>
	</div>
</template>

<script>
	export default {
		name: 'stock',
		props: ['query', 'summary','share'],
		data(){
			return{
				currentDate: this.dateToString(),
			}
		},
		created(){

		},
		methods:{
			dateToString() {
				var _date = new Date();
				var year = _date.getFullYear();
				var month = _date.getMonth() + 1;
				var day = _date.getDate();
				var currentDate = year.toString() + '-' + month.toString() + '-' + day.toString();
				return currentDate
			},
		},
		
	}
</script>

<style>
</style>
