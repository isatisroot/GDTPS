<template>
	<div>
		<el-dialog :visible.sync="dialogFormVisible"><span slot="title" style="margin-left: 400px;font-size: 30px;">新增会议</span>
			<el-form :model="form">
				<el-form-item label="会议名称" :label-width="formLabelWidth">
					<el-input v-model="form.name" autocomplete="off"></el-input>
				</el-form-item>
		
				<el-form-item label="会议时间" :label-width="formLabelWidth">
					<el-col :span="10" style="padding-left: 0px">
						<el-date-picker type="date" placeholder="选择日期" v-model="form.date1" value-format="yyyy-MM-dd"></el-date-picker>
					</el-col>
					<!-- <el-col class="line" :span="2">-</el-col> -->
					<el-col :span="10">
						<el-time-picker placeholder="选择时间" v-model="form.date2" format="HH:mm" value-format="HH:mm"></el-time-picker>
					</el-col>
				</el-form-item>
				<el-form-item label="会议地点" :label-width="formLabelWidth" default-first-option>
					<!-- <el-cascader :options="options" v-model="form.address"></el-cascader> -->
					<el-input  v-model="form.address"></el-input>
				</el-form-item>
				<el-form-item label="会议议案" :label-width="formLabelWidth">
					<!-- <template slot-scope="scope"> -->
					<div style="float: left; width: 90%">
						<!-- <li v-for="(val, id) in motion.list" :key="id" style="list-style-type:none;">
							<el-input type="text" style="margin-bottom: 5px;" v-model="val.text"></el-input>
						</li> -->
						<!-- 使用作用域插槽，el-table是子组件，现在往子组件传<template>的内容，并获取里面的内容 -->
						<el-table :data="motionArray" :show-header="false">
							<el-table-column prop=motion >
								<template slot-scope="scope">
									<el-input v-model="motionArray[scope.$index].motion"></el-input>
								</template>
							</el-table-column>
						</el-table>
						<!-- <el-input type="text" style="margin-bottom: 5px;"></el-input>
						<el-input type="text" style="margin-bottom: 5px;"></el-input> -->
					</div>
					<div style="float:right">
						<el-button icon="el-icon-circle-plus" type="success" @click="addMotion"></el-button>
					</div>
		
		
					<!-- </template> -->
				</el-form-item>
			</el-form>
			<div class="edit_dev">
				<el-transfer v-model="value" :data="gddata" :titles="['可添加股东信息列表', '已添加股东信息列表']"></el-transfer>
			</div>
		
			<div slot="footer" class="dialog-footer">
				<el-button @click="dialogFormVisible = false">取 消</el-button>
				<el-button type="primary" @click="submitAdd">确 定</el-button>
				<!-- <el-button type="primary">
					<router-link :to="'/table'"><span style="color: white;">确定</span></router-link>
				</el-button> -->
			</div>
		</el-dialog>
		
	</div>
</template>

<script>
	export default{
		name: 'newmeeting',
		data(){
			
		}
	}
</script>

<style>
</style>
