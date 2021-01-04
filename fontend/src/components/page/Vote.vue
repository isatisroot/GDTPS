<template>
	<div>
		<!-- <button v-print="'#printTest'">打印</button> -->
		<div id="printVote">
			　　
			<div style="page-break-after:always" v-for="row in checkedData" :key="row.gdxm">
				<h3 class="titile3" align="center" >佛山电器照明股份有限公司</h3>
				<h2 class="titile2" align="center">{{year+name}}议案表决票</h2>
				<table border="1" style="width: 50%;margin:auto;text-align: center;">
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
				<p style="margin-left: 160px;margin-top: 20px;">说明：每项议案均有一张表决票,请在赞成、反对或弃权栏中选择一项使用“✓”符号投票表决，多选无效</p>
				<table border="1" style="width: 80%;margin:auto;text-align: center;">
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
			</div>

			
		</div>

		<!-- <el-button type="success" icon="el-icon-printer">打印议案表决票</el-button> -->
		<!-- <el-table :data="content" border align="center" >
				</el-table-column>
				<el-table-column prop="gdxm" label="股东姓名(单位)"  align="center">
				</el-table-column>
				<el-table-column prop="gddmk" label="股东代码"  align="center">
				</el-table-column>
				<el-table-column  label="股份数" align="center">
					<el-table-column prop="gzA" label="A股"  align="center">
					</el-table-column>
					<el-table-column prop="gzB" label="B股" align="center">
					</el-table-column>		
				</el-table-column>		
			</el-table> -->
		<!-- <div style="page-break-after:always">我是第二个分页</div>　　 -->


	</div>
</template>

<script>
	export default {
		name: 'vote',
		props: ['year', 'name', 'checkedData', 'motion'],
		data() {
			return {
				datas: ['a', 'b']
			}
		},
		created() {

		},
		methods: {},
	}
</script>

<style>
	.title2{
		margin-top: 30px;
		margin-bottom: 20px;
	
	}
	.titile3 {
		margin-top: 30px;
		margin-bottom: 20px;
	}
</style>
