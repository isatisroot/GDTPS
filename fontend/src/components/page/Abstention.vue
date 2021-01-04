<template>
	<div>

			<h3 align="center">佛山电器照明公司</h3>
			<h2 align="center">2020第二次临时股东大会议案表决投反对票、弃权票统计表</h2>
			<el-table style="width: 100%" align="center">
				<el-table-column prop="proposalNum" label="议案编号" width="150" align="center">
				</el-table-column>
				<el-table-column prop="subNum" label="子编号" width="70" align="center">
				</el-table-column>
				<el-table-column prop="theme" label="议案主题" width="200" align="center">
				</el-table-column>


				<el-table-column label="反对票" align="center">
					<el-table-column prop="shareNum" label="股份数" width="220" align="center">
					</el-table-column>
					<el-table-column prop="subtotal" label="小计" width="120" align="center">
					</el-table-column>
					<el-table-column prop="total" label="合计" width="120" align="center">
					</el-table-column>
				</el-table-column>

				<el-table-column label="弃权票" align="center">
					<el-table-column prop="shareNum" label="股份数" width="220" align="center">
					</el-table-column>
					<el-table-column prop="subtotal" label="小计" width="120" align="center">
					</el-table-column>
					<el-table-column prop="total" label="合计" width="120" align="center">
					</el-table-column>
				</el-table-column>

				<el-table-column label="采用累积投票" width="105">
					<el-checkbox></el-checkbox>
				</el-table-column>
				<el-table-column label="存在回避票" width="105">
					<el-checkbox></el-checkbox>
				</el-table-column>

				<el-table-column label="回避票数" align="center">
					<el-table-column prop="AShare" label="A股" width="220" align="center">
					</el-table-column>
					<el-table-column prop="BShare" label="B股" width="120" align="center">
					</el-table-column>
				</el-table-column>

				<el-table-column label="回避表述" width="200" align="center">
				</el-table-column>
				</el-table-column>
			</el-table>
	</div>
</template>

<script>
	export default{
		name: 'abstention',
		props: ['year', 'name']
	}
</script>

<style>
</style>
