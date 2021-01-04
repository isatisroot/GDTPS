<template>
	<div id="printStock">
		<h3 align="center">佛山电器照明股份有限公司</h3>
		<h2 align="center">{{query.year+query.name}}股东、股份数统计表</h2>
		<p>公司总股本：{{statistics.sumAStock + statistics.sumBStock}},其中A股：{{statistics.sumAStock}},B股：{{statistics.sumBStock}}</p>
		<table border="1" style="width: 50%;margin:auto;text-align: center;">
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
		</table>
		
	</div>
</template>

<script>
	export default {
		name: 'stock',
		props: ['query', 'statistics'],
		data(){
			return{}
		},
		created(){
			// axios.get(this.host + 'get_detail/' + this.query.year + '/' + this.query.name)
			// 	.then(response => (
			// 		this.tableData = response.data,
			// 		this.pageTotal = 15
			// 	)).catch(error => {
			// 		alert('error')
			// 		console.log(error.response.data);
			// 	})
		},
		methods:{},
		
	}
</script>

<style>
</style>
