<template>
	<div>
		<el-button class="button" icon="el-icon-printer" v-print="'#printStock'">打印</el-button>
	
		<div id="printStock">
		<p class="title1" >佛山电器照明股份有限公司</p>
		<p  class="title2" align="center">{{query.year+query.name}}股东、股份数统计表</p>
		<p class="text">公司总股本：{{totalShare}}股，其中A股：{{AShareTotal}}股，B股：{{BShareTotal}}股</p>
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
				<td>{{statistics.sumA}}</td>
				<td>{{statistics.sumAStock}}</td>
				<td>{{statistics.percentA}}</td>
				<td></td>
			</tr>
			<tr>
				<td>B股</td>
				<td>{{statistics.sumB}}</td>
				<td>{{statistics.sumBStock}}</td>
				<td>{{statistics.percentB}}</td>
				<td></td>
			</tr>
			<tr>
				<td>合计</td>
				<td>{{statistics.sumB + statistics.sumA}}</td>
				<td>{{statistics.sumBStock + statistics.sumAStock}}</td>
				<td>{{statistics.percentB}}</td>
				<td></td>
			</tr>
		</table>
		<p align="right" class="bottom-p">统计人签字：____________</p>
		<p> 注：统计至开会开始前{{date}},请在{{date}}前送到主席台</p>
		<p align="right" class="bottom-p">佛山电器照明股份有限公司</p>
		<p align="right" class="bottom-p">{{currentDate}}</p>
	</div>
	</div>
</template>

<script>
	export default {
		name: 'stock',
		props: ['query', 'statistics','totalShare', 'AShareTotal', 'BShareTotal', 'date'],
		data(){
			return{}
		},
		created(){

		},
		methods:{},
		
	}
</script>

<style>
</style>
